from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.audio import get_audio_store
from app.db import get_session
from app.identity import AuthenticatedIdentity, get_current_identity
from app.main import app
from app.models import (
    Campaign,
    CampaignRewardRule,
    Card,
    ConsentGrant,
    ConsentScope,
    User,
    VerifierQualification,
)


def test_governed_peer_flow_through_public_api(db_session, tmp_path):
    now = datetime.now(timezone.utc)
    speaker = User(
        id=uuid.uuid4(),
        provider_subject="e2e-speaker",
        declared_languages=["tn"],
        age_confirmed_at=now,
        created_at=now,
    )
    verifiers = [
        User(
            id=uuid.uuid4(),
            provider_subject=f"e2e-verifier-{index}",
            declared_languages=["tn"],
            age_confirmed_at=now,
            created_at=now,
        )
        for index in range(3)
    ]
    campaign = Campaign(
        id=uuid.uuid4(),
        name="Governed E2E",
        language="tn",
        budget_cents=1000,
        funded_cents=1000,
        committed_cents=0,
        provider_mode="DEMO_PROVIDER",
    )
    rule = CampaignRewardRule(
        id=uuid.uuid4(),
        campaign_id=campaign.id,
        version="e2e-v1",
        contribution_reward_cents=100,
        effective_from=now,
    )
    card = Card(
        id=uuid.uuid4(),
        language="tn",
        target="kgomo",
        blocked_words=["a", "b", "c", "d"],
        accepted_answers=["kgomo", "kgomo"],
        distractors=["x", "y", "z"],
        campaign_id=campaign.id,
        active=True,
    )
    db_session.add_all([speaker, *verifiers, campaign, rule, card])
    db_session.flush()
    db_session.add_all(
        [
            ConsentGrant(user_id=speaker.id, version="consent-v1", scope=ConsentScope.RECORD_PROCESS_ROUND),
            ConsentGrant(user_id=speaker.id, version="consent-v1", scope=ConsentScope.ASSIGNED_VERIFIER_PLAYBACK),
            *[
                VerifierQualification(
                    user_id=verifier.id,
                    language="tn",
                    qualified_at=now,
                    reviewed_by=speaker.id,
                )
                for verifier in verifiers
            ],
        ]
    )
    db_session.commit()

    from app.storage import LocalAudioObjectStore

    store = LocalAudioObjectStore(tmp_path, secret=b"e2e-audio-secret")
    current = {"identity": AuthenticatedIdentity(speaker.id, speaker.provider_subject)}
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_identity] = lambda: current["identity"]
    app.dependency_overrides[get_audio_store] = lambda: store

    try:
        with TestClient(app) as client:
            created = client.post("/contributions", json={"card_id": str(card.id)})
            assert created.status_code == 201, created.text
            contribution_id = created.json()["id"]

            upload = client.post(f"/contributions/{contribution_id}/audio/uploads")
            assert upload.status_code == 200, upload.text
            audio_id = upload.json()["audio_object_id"]
            body = b"governed voice"
            uploaded = client.put(f"/private-audio/uploads/{audio_id}", content=body)
            assert uploaded.status_code == 200, uploaded.text
            finalised = client.post(
                f"/contributions/{contribution_id}/audio/finalise",
                json={
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "mime_type": "audio/webm",
                    "codec": "opus",
                    "duration_ms": 1000,
                    "byte_length": len(body),
                },
            )
            assert finalised.status_code == 200, finalised.text

            playback = client.post(f"/contributions/{contribution_id}/playback")
            assert playback.status_code == 200, playback.text
            playback_path = playback.json()["url"]

            assignment_ids = []
            for verifier in verifiers[:2]:
                current["identity"] = AuthenticatedIdentity(verifier.id, verifier.provider_subject)
                assignment = client.get(
                    f"/assignments/next?contribution_id={contribution_id}&language=tn"
                )
                assert assignment.status_code == 200, assignment.text
                assignment_ids.append(assignment.json()["id"])
                answer = client.post(
                    f"/assignments/{assignment_ids[-1]}/answer",
                    json={"answer_text": " KGOMO ", "violation_vote": False},
                )
                assert answer.status_code == 200, answer.text

            current["identity"] = AuthenticatedIdentity(speaker.id, speaker.provider_subject)
            result = client.get(f"/contributions/{contribution_id}/result")
            assert result.status_code == 200, result.text
            assert result.json() == {
                "status": "RESOLVED",
                "understood": True,
                "corpus_eligible": True,
                "reason": "understood by both verifiers, audio quality passed, consent active",
            }
            assert client.get(playback_path).status_code == 200
            assert db_session.query(ConsentGrant).filter_by(
                user_id=speaker.id, scope=ConsentScope.RETAIN_MODEL_DEVELOPMENT
            ).count() == 0

            revoked = client.post(
                "/consents/RECORD_PROCESS_ROUND/revoke",
                params={"reason": "speaker withdrew recording replay"},
            )
            assert revoked.status_code == 200, revoked.text
            assert client.get(playback_path).status_code == 403

            current["identity"] = AuthenticatedIdentity(speaker.id, speaker.provider_subject)
            revoked_peer_scope = client.post(
                "/consents/ASSIGNED_VERIFIER_PLAYBACK/revoke",
                params={"reason": "speaker withdrew verifier playback"},
            )
            assert revoked_peer_scope.status_code == 200, revoked_peer_scope.text
            current["identity"] = AuthenticatedIdentity(verifiers[2].id, verifiers[2].provider_subject)
            after_revoke = client.get(
                f"/assignments/next?contribution_id={contribution_id}&language=tn"
            )
            assert after_revoke.status_code == 404
            assert after_revoke.json()["detail"]["code"] == "NO_ASSIGNMENT"
    finally:
        app.dependency_overrides.clear()
