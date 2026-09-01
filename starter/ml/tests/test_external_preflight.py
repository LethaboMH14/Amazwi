from pathlib import Path

import pytest

from amazwi_ml.external import (
    PreflightRequired,
    TaskProhibited,
    approve_preflight,
    load_registry,
    require_download_preflight,
)


REGISTRY = Path(__file__).parents[1] / "registry" / "external_datasets.yaml"


@pytest.fixture
def registry():
    return load_registry(REGISTRY)


@pytest.mark.parametrize(
    "dataset_id",
    ["swivuriso", "afriswitch", "common-voice-26-setswana", "nchlt", "lwazi", "fleurs"],
)
def test_download_without_approved_preflight_is_refused(registry, dataset_id):
    with pytest.raises(PreflightRequired):
        require_download_preflight(registry, None, dataset_id=dataset_id, intended_task="ASR_TRAINING")


def test_swivuriso_rejects_synthesis_task(registry):
    with pytest.raises(TaskProhibited):
        approve_preflight(
            registry,
            dataset_id="swivuriso",
            exact_revision="0123456789abcdef",
            intended_task="TTS",
            reviewer="data-steward@example.test",
            reviewed_at="2026-09-01T00:00:00Z",
            terms_accepted=True,
        )


def test_registry_has_exact_policy_and_stable_hash(registry):
    assert registry.datasets["swivuriso"].allowed_tasks == ("ASR_TRAINING", "ASR_EVALUATION")
    assert registry.datasets["afriswitch"].allowed_tasks == ("ASR_EVALUATION",)
    assert registry.datasets["nchlt"].state == "BLOCKED_METADATA_REVIEW"
    assert len(registry.registry_sha256) == 64
    assert registry.registry_sha256 == load_registry(REGISTRY).registry_sha256


def test_approved_preflight_unlocks_only_matching_revision_and_task(registry):
    evidence = approve_preflight(
        registry,
        dataset_id="swivuriso",
        exact_revision="0123456789abcdef0123456789abcdef01234567",
        intended_task="ASR_TRAINING",
        reviewer="data-steward@example.test",
        reviewed_at="2026-09-01T00:00:00Z",
        terms_accepted=True,
    )
    spec = require_download_preflight(
        registry, evidence, dataset_id="swivuriso", intended_task="ASR_TRAINING"
    )
    assert spec.dataset_id == "swivuriso"
    assert spec.exact_revision == evidence.exact_revision
    with pytest.raises(PreflightRequired):
        require_download_preflight(
            registry,
            evidence,
            dataset_id="swivuriso",
            intended_task="ASR_EVALUATION",
        )
