"""Reviewed external-source registry and a download-before-network safety gate."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

import yaml


class ExternalRegistryError(ValueError):
    """The reviewed registry or requested dataset is invalid."""


class PreflightRequired(PermissionError):
    """No matching approved preflight evidence exists."""


class TaskProhibited(PermissionError):
    """The registry does not permit the requested task."""


@dataclass(frozen=True)
class ExternalDatasetSpec:
    dataset_id: str
    name: str
    url: str
    state: str
    licence: str
    restrictions: tuple[str, ...]
    allowed_tasks: tuple[str, ...]
    exact_revision_required: bool = True
    release: str | None = None
    exact_revision: str | None = None


@dataclass(frozen=True)
class ExternalRegistry:
    datasets: Mapping[str, ExternalDatasetSpec]
    registry_sha256: str
    path: str


@dataclass(frozen=True)
class PreflightEvidence:
    dataset_id: str
    exact_revision: str
    intended_task: str
    reviewer: str
    reviewed_at: str
    terms_accepted: bool
    decision: str
    registry_sha256: str

    def model_dump(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "exact_revision": self.exact_revision,
            "intended_task": self.intended_task,
            "reviewer": self.reviewer,
            "reviewed_at": self.reviewed_at,
            "terms_accepted": self.terms_accepted,
            "decision": self.decision,
            "registry_sha256": self.registry_sha256,
        }


def _canonical_registry_bytes(raw: dict[str, Any]) -> bytes:
    return (json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def load_registry(path: str | Path) -> ExternalRegistry:
    path = Path(path)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        entries = raw["datasets"]
    except (OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        raise ExternalRegistryError(f"invalid registry: {path}") from exc
    datasets: dict[str, ExternalDatasetSpec] = {}
    for dataset_id, value in entries.items():
        if not isinstance(value, dict):
            raise ExternalRegistryError(f"invalid dataset entry: {dataset_id}")
        datasets[dataset_id] = ExternalDatasetSpec(
            dataset_id=dataset_id,
            name=str(value.get("name", dataset_id)),
            url=str(value.get("url", "")),
            state=str(value.get("state", "")),
            licence=str(value.get("licence", "")),
            restrictions=tuple(str(x) for x in value.get("restrictions", [])),
            allowed_tasks=tuple(str(x) for x in value.get("allowed_tasks", [])),
            exact_revision_required=bool(value.get("exact_revision_required", True)),
            release=value.get("release"),
        )
    return ExternalRegistry(datasets, hashlib.sha256(_canonical_registry_bytes(raw)).hexdigest(), str(path))


def _spec(registry: ExternalRegistry, dataset_id: str) -> ExternalDatasetSpec:
    try:
        return registry.datasets[dataset_id]
    except KeyError as exc:
        raise ExternalRegistryError(f"unknown dataset: {dataset_id}") from exc


def approve_preflight(
    registry: ExternalRegistry,
    *,
    dataset_id: str,
    exact_revision: str,
    intended_task: str,
    reviewer: str,
    reviewed_at: str,
    terms_accepted: bool,
) -> PreflightEvidence:
    spec = _spec(registry, dataset_id)
    if intended_task not in spec.allowed_tasks:
        raise TaskProhibited(f"{dataset_id} does not permit {intended_task}")
    if spec.state != "APPROVED_METADATA":
        raise PreflightRequired(f"{dataset_id} is {spec.state}")
    if not exact_revision or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{7,127}", exact_revision):
        raise PreflightRequired("exact revision is required")
    if not reviewer or not reviewed_at or not terms_accepted:
        raise PreflightRequired("reviewer, review timestamp, and terms acceptance are required")
    return PreflightEvidence(dataset_id, exact_revision, intended_task, reviewer, reviewed_at, terms_accepted, "APPROVED", registry.registry_sha256)


def require_download_preflight(
    registry: ExternalRegistry,
    evidence: PreflightEvidence | None,
    *,
    dataset_id: str,
    intended_task: str,
) -> ExternalDatasetSpec:
    spec = _spec(registry, dataset_id)
    if evidence is None or evidence.decision != "APPROVED":
        raise PreflightRequired("PREFLIGHT_REQUIRED")
    if evidence.registry_sha256 != registry.registry_sha256:
        raise PreflightRequired("registry hash does not match evidence")
    if evidence.dataset_id != dataset_id or evidence.intended_task != intended_task:
        raise PreflightRequired("preflight dataset/task does not match request")
    if not evidence.exact_revision:
        raise PreflightRequired("exact revision is required")
    if intended_task not in spec.allowed_tasks:
        raise TaskProhibited(f"{dataset_id} does not permit {intended_task}")
    if spec.state != "APPROVED_METADATA":
        raise PreflightRequired(f"{dataset_id} is {spec.state}")
    return replace(spec, exact_revision=evidence.exact_revision)
