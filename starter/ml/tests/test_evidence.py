import hashlib
import json

import pytest

from amazwi_ml.evidence import EvidenceRun, IncompleteEvidence, generate_model_card, sha256_file, write_evidence_index

MANIFEST = "a" * 64


def test_sha256_file_matches_hashlib(tmp_path):
    path = tmp_path / "artefact.bin"
    path.write_bytes(b"amazwi")
    assert sha256_file(path) == hashlib.sha256(b"amazwi").hexdigest()


def test_generate_model_card_requires_full_length_manifest_hash():
    run = EvidenceRun(
        candidate_id="c1",
        promoted=True,
        reasons=(),
        manifest_sha256="short",
        metrics={"wer": 0.10},
    )
    with pytest.raises(IncompleteEvidence):
        generate_model_card(run)


def test_generate_model_card_promoted_states_decision_and_no_disclaimer():
    run = EvidenceRun(
        candidate_id="isizulu-asr-v2",
        promoted=True,
        reasons=(),
        manifest_sha256=MANIFEST,
        metrics={"wer": 0.18, "cer": 0.09},
    )
    card = generate_model_card(run)
    assert "Promotion decision: PROMOTED" in card
    assert f"`{MANIFEST}`" in card
    assert "No held-out improvement claim is made." not in card


def test_generate_model_card_not_promoted_states_decision_and_disclaimer():
    run = EvidenceRun(
        candidate_id="isizulu-asr-v2",
        promoted=False,
        reasons=("WER_INSUFFICIENT",),
        manifest_sha256=MANIFEST,
        metrics={"wer": 0.196},
    )
    card = generate_model_card(run)
    assert "Promotion decision: NOT PROMOTED" in card
    assert "No held-out improvement claim is made." in card
    assert "WER_INSUFFICIENT" in card


def test_generate_model_card_never_omits_prohibited_use():
    run = EvidenceRun(
        candidate_id="quality-risk-v1",
        promoted=True,
        reasons=(),
        manifest_sha256=MANIFEST,
        metrics={"brier": 0.15},
    )
    card = generate_model_card(run)
    assert "eligibility, rewards, voice cloning" in card


def test_generate_model_card_all_gates_passed_when_no_reasons():
    run = EvidenceRun(
        candidate_id="c1",
        promoted=True,
        reasons=(),
        manifest_sha256=MANIFEST,
        metrics={},
    )
    card = generate_model_card(run)
    assert "Reasons: all gates passed" in card


def test_generate_model_card_metrics_are_deterministically_ordered():
    run = EvidenceRun(
        candidate_id="c1",
        promoted=True,
        reasons=(),
        manifest_sha256=MANIFEST,
        metrics={"z": 1.0, "a": 2.0, "m": 3.0},
    )
    card = generate_model_card(run)
    assert json.dumps({"a": 2.0, "m": 3.0, "z": 1.0}, sort_keys=True) in card


def test_write_evidence_index_hashes_every_artefact_and_returns_index_hash(tmp_path):
    artefact_a = tmp_path / "a.json"
    artefact_a.write_bytes(b"alpha")
    artefact_b = tmp_path / "b.json"
    artefact_b.write_bytes(b"beta")
    output = tmp_path / "out" / "evidence_index.json"

    returned_hash = write_evidence_index([artefact_b, artefact_a], output)

    assert output.exists()
    payload = json.loads(output.read_text())
    assert payload == {
        "artefacts": {
            str(artefact_a): hashlib.sha256(b"alpha").hexdigest(),
            str(artefact_b): hashlib.sha256(b"beta").hexdigest(),
        }
    }
    assert returned_hash == sha256_file(output)


def test_write_evidence_index_is_deterministic_regardless_of_input_order(tmp_path):
    artefact_a = tmp_path / "a.json"
    artefact_a.write_bytes(b"alpha")
    artefact_b = tmp_path / "b.json"
    artefact_b.write_bytes(b"beta")
    output_1 = tmp_path / "out1.json"
    output_2 = tmp_path / "out2.json"

    hash_1 = write_evidence_index([artefact_a, artefact_b], output_1)
    hash_2 = write_evidence_index([artefact_b, artefact_a], output_2)

    assert hash_1 == hash_2
    assert output_1.read_text() == output_2.read_text()
