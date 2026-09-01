import pytest

from amazwi_ml.external import (
    PreflightEvidence,
    PreflightRequired,
    TaskProhibited,
    approve_preflight,
    load_registry,
)

REGISTRY = {
    "datasets": {
        "swivuriso": {
            "revision_required": True,
            "allowed_tasks": ["ASR_TRAINING", "ASR_EVALUATION"],
            "prohibited_tasks": ["TTS", "VOICE_CLONING", "SPEECH_SYNTHESIS", "HUMAN_VOICE_REPLICATION"],
        },
        "afriswitch": {
            "revision_required": True,
            "allowed_tasks": ["ASR_EVALUATION"],
            "acquisition_blocked": True,
        },
        "nchlt": {"allowed_tasks": []},
    }
}


def test_load_registry_reads_the_real_repository_file():
    from pathlib import Path
    registry = load_registry(Path(__file__).parent.parent / "registry" / "external_datasets.yaml")
    assert "swivuriso" in registry["datasets"]
    assert "afriswitch" in registry["datasets"]


def test_approve_preflight_succeeds_for_an_allowed_task():
    evidence = approve_preflight(
        REGISTRY,
        dataset_id="swivuriso",
        exact_revision="rev-1",
        intended_task="ASR_TRAINING",
        reviewer="sbu",
        reviewed_at="2026-09-01T00:00:00Z",
        terms_accepted=True,
    )
    assert evidence.decision == "APPROVED"
    assert evidence.dataset_id == "swivuriso"


def test_approve_preflight_blocks_prohibited_task():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="swivuriso",
            exact_revision="rev-1",
            intended_task="VOICE_CLONING",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_approve_preflight_blocks_task_not_in_allowed_list():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="swivuriso",
            exact_revision="rev-1",
            intended_task="SPEAKER_IDENTIFICATION",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_approve_preflight_blocks_when_terms_not_accepted():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="swivuriso",
            exact_revision="rev-1",
            intended_task="ASR_TRAINING",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=False,
        )


def test_approve_preflight_blocks_missing_exact_revision():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="swivuriso",
            exact_revision="",
            intended_task="ASR_TRAINING",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_approve_preflight_blocks_unknown_dataset():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="does-not-exist",
            exact_revision="rev-1",
            intended_task="ASR_TRAINING",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_approve_preflight_blocks_acquisition_blocked_dataset_even_for_allowed_task():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="afriswitch",
            exact_revision="rev-1",
            intended_task="ASR_EVALUATION",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_approve_preflight_blocks_dataset_with_empty_allowed_tasks():
    with pytest.raises(TaskProhibited):
        approve_preflight(
            REGISTRY,
            dataset_id="nchlt",
            exact_revision="rev-1",
            intended_task="ASR_TRAINING",
            reviewer="sbu",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


# ---------------------------------------------------------------------------
# require_download_preflight -- the actual hard gate a download call must pass
# ---------------------------------------------------------------------------

from amazwi_ml.external import require_download_preflight


def test_require_download_preflight_passes_with_matching_approved_evidence():
    evidence = approve_preflight(
        REGISTRY, dataset_id="swivuriso", exact_revision="rev-1", intended_task="ASR_TRAINING",
        reviewer="sbu", reviewed_at="2026-09-01T00:00:00Z", terms_accepted=True,
    )
    spec = require_download_preflight(REGISTRY, evidence, dataset_id="swivuriso", intended_task="ASR_TRAINING")
    assert spec is REGISTRY["datasets"]["swivuriso"]


def test_require_download_preflight_rejects_no_evidence():
    with pytest.raises(PreflightRequired):
        require_download_preflight(REGISTRY, None, dataset_id="swivuriso", intended_task="ASR_TRAINING")


def test_require_download_preflight_rejects_evidence_for_a_different_dataset():
    evidence = approve_preflight(
        REGISTRY, dataset_id="swivuriso", exact_revision="rev-1", intended_task="ASR_TRAINING",
        reviewer="sbu", reviewed_at="2026-09-01T00:00:00Z", terms_accepted=True,
    )
    with pytest.raises(PreflightRequired):
        require_download_preflight(
            REGISTRY, evidence, dataset_id="common-voice-26-setswana", intended_task="ASR_TRAINING",
        )


def test_require_download_preflight_rejects_evidence_for_a_different_task():
    evidence = approve_preflight(
        REGISTRY, dataset_id="swivuriso", exact_revision="rev-1", intended_task="ASR_TRAINING",
        reviewer="sbu", reviewed_at="2026-09-01T00:00:00Z", terms_accepted=True,
    )
    with pytest.raises(PreflightRequired):
        require_download_preflight(REGISTRY, evidence, dataset_id="swivuriso", intended_task="ASR_EVALUATION")


def test_require_download_preflight_rejects_evidence_from_a_stale_registry():
    evidence = approve_preflight(
        REGISTRY, dataset_id="swivuriso", exact_revision="rev-1", intended_task="ASR_TRAINING",
        reviewer="sbu", reviewed_at="2026-09-01T00:00:00Z", terms_accepted=True,
    )
    mutated_registry = {"datasets": {**REGISTRY["datasets"], "swivuriso": {**REGISTRY["datasets"]["swivuriso"], "allowed_tasks": ["ASR_TRAINING"]}}}
    with pytest.raises(PreflightRequired):
        require_download_preflight(mutated_registry, evidence, dataset_id="swivuriso", intended_task="ASR_TRAINING")


def test_require_download_preflight_rejects_a_forged_not_approved_decision():
    forged = PreflightEvidence(
        dataset_id="swivuriso", exact_revision="rev-1", intended_task="ASR_TRAINING",
        reviewer="sbu", decision="PENDING", registry_sha256="0" * 64,
    )
    with pytest.raises(PreflightRequired):
        require_download_preflight(REGISTRY, forged, dataset_id="swivuriso", intended_task="ASR_TRAINING")
