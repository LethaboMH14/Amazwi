"""Honest, artefact-derived evidence and model-card primitives."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Sequence

class IncompleteEvidence(ValueError):
    pass

@dataclass(frozen=True)
class EvidenceRun:
    candidate_id: str
    promotion_promoted: bool = False
    promotion_reasons: tuple[str, ...] = ()
    metrics: dict[str, Any] = field(default_factory=dict)
    baseline_metrics: dict[str, Any] = field(default_factory=dict)
    languages: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    dataset_manifest_sha256: str = ""
    evaluation_manifest_sha256: str = ""
    source_classes: tuple[str, ...] = ()
    licence_summary: str = ""
    speaker_split_policy: str = ""
    acceptance_policy: str = ""
    slices: dict[str, Any] = field(default_factory=dict)
    ablations: dict[str, Any] = field(default_factory=dict)
    seed: int | None = None
    artefact_hashes: dict[str, str] = field(default_factory=dict)
    budget_entry: dict[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()
    consent_revocation_statement: str = ""
    status: str = ""
    intended_uses: tuple[str, ...] = ()
    prohibited_uses: tuple[str, ...] = ()


def _required(run: EvidenceRun) -> None:
    missing = []
    for name in ("candidate_id", "dataset_manifest_sha256", "evaluation_manifest_sha256", "licence_summary", "speaker_split_policy", "acceptance_policy", "status"):
        if not getattr(run, name): missing.append(name)
    if not run.artefact_hashes: missing.append("artefact_hashes")
    if missing: raise IncompleteEvidence("missing evidence: " + ", ".join(missing))


def generate_model_card(run: EvidenceRun) -> str:
    _required(run)
    decision = "PROMOTED" if run.promotion_promoted else "NOT PROMOTED"
    lines = [f"# Model card: {run.candidate_id}", "", f"Promotion decision: {decision}"]
    if not run.promotion_promoted: lines.append("No held-out improvement claim is made.")
    intended = [f"- {x}" for x in run.intended_uses] or ["- Governed research evaluation only."]
    prohibited = [f"- {x}" for x in run.prohibited_uses] or ["- Eligibility, rewards, identity decisions, or unrestricted deployment."]
    limitations = [f"- {x}" for x in run.limitations] or ["- No production claim is made."]
    lines += ["", "## Intended use", *intended, "## Prohibited use", *prohibited, "## Data and evaluation"]
    lines += [f"- Dataset manifest SHA-256: `{run.dataset_manifest_sha256}`", f"- Evaluation manifest SHA-256: `{run.evaluation_manifest_sha256}`", f"- Languages: {', '.join(run.languages) or 'not specified'}", f"- Domains: {', '.join(run.domains) or 'not specified'}", f"- Source classes: {', '.join(run.source_classes) or 'not specified'}", f"- Licence/restrictions: {run.licence_summary}", f"- Speaker split policy: {run.speaker_split_policy}", "", "## Metrics", f"- Baseline: `{json.dumps(run.baseline_metrics, sort_keys=True)}`", f"- Candidate: `{json.dumps(run.metrics, sort_keys=True)}`", f"- Slices: `{json.dumps(run.slices, sort_keys=True)}`", "", "## Governance", f"- Acceptance policy: {run.acceptance_policy}", f"- Reason codes: {', '.join(sorted(run.promotion_reasons)) or 'none'}", f"- Seed: {run.seed}", f"- Consent and revocation: {run.consent_revocation_statement or 'Only separately opted-in, unrevoked data may be used.'}", f"- Run status: {run.status}", "", "## Limitations", *limitations]
    return "\n".join(lines) + "\n"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_evidence_index(paths: Sequence[Path], output: Path) -> str:
    artefacts = [str(Path(path)) for path in paths]
    if len(set(artefacts)) != len(artefacts): raise ValueError("duplicate artefact path")
    index = {"artefacts": sorted(artefacts), "sha256": {str(Path(path)): _sha256(Path(path)) for path in paths}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return _sha256(output)
