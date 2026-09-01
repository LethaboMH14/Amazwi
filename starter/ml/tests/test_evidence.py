import hashlib, json
import pytest
from amazwi_ml.evidence import EvidenceRun, IncompleteEvidence, generate_model_card, write_evidence_index


def run(**kwargs):
    base = dict(candidate_id="candidate", dataset_manifest_sha256="a"*64, evaluation_manifest_sha256="b"*64, licence_summary="synthetic", speaker_split_policy="speaker-group", acceptance_policy="fixed", status="EVALUATED", artefact_hashes={"metrics":"c"*64})
    base.update(kwargs)
    return EvidenceRun(**base)


def test_failed_promotion_is_honest():
    card = generate_model_card(run(promotion_reasons=("CER_REGRESSION",)))
    assert "Promotion decision: NOT PROMOTED" in card
    assert "No held-out improvement claim is made." in card
    assert "improved model deployed" not in card.lower()


def test_incomplete_evidence_is_rejected():
    with pytest.raises(IncompleteEvidence):
        generate_model_card(EvidenceRun(candidate_id="missing"))


def test_evidence_index_hashes_declared_files(tmp_path):
    files = [tmp_path / "b.txt", tmp_path / "a.txt"]
    for path in files: path.write_text(path.stem, encoding="utf-8")
    output = tmp_path / "evidence-index.json"
    digest = write_evidence_index(files, output)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert digest == hashlib.sha256(output.read_bytes()).hexdigest()
    assert data["artefacts"] == sorted(str(path) for path in files)
