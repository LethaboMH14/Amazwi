"""Atomic, filesystem-backed GPU-hour budget ledger."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib, json, os, re
from pathlib import Path

PHASE_CAPS = {"PREFLIGHT_SPLITS": 6.0, "FIXED_TOURNAMENT": 8.0, "ISIZULU_ADAPTATION": 16.0, "SETSWANA_ADAPTATION": 16.0, "TABULAR": 8.0, "TABULAR_CHALLENGERS": 8.0, "REPRODUCIBILITY": 6.0}
ACCOUNTS = {"team-sonar-a", "team-sonar-b"}
_HASH = re.compile(r"^[0-9a-f]{64}$")

class BudgetError(ValueError): pass
class BudgetExceeded(BudgetError): pass
class AccountBudgetExceeded(BudgetError): pass
class PhaseBudgetExceeded(BudgetError): pass
class DuplicateRun(BudgetError): pass

@dataclass(frozen=True)
class BudgetReservation:
    run_id: str; account_alias: str; phase: str; requested_gpu_hours: float; manifest_sha256: str; config_sha256: str; status: str = "RESERVED"

@dataclass(frozen=True)
class BudgetEntry:
    run_id: str; account_alias: str; phase: str; requested_gpu_hours: float; actual_gpu_hours: float | None; manifest_sha256: str; config_sha256: str; artefact_sha256: str | None; status: str


def _load(path: Path) -> dict:
    if not path.exists(): return {"version": 1, "entries": []}
    data = json.loads(path.read_text(encoding="utf-8")); data.setdefault("entries", []); return data

def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["entries"] = sorted(data["entries"], key=lambda item: item["run_id"])
    raw = json.dumps(data, sort_keys=True, indent=2) + "\n"
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
    os.replace(temp, path)

def _hash(value: str, name: str) -> None:
    if not isinstance(value, str) or not _HASH.fullmatch(value): raise BudgetError(f"invalid {name} sha256")

def _hours(entries: list[dict], account: str | None = None, phase: str | None = None) -> float:
    return sum(float(e.get("actual_gpu_hours") if e.get("status") == "COMPLETED" else e.get("requested_gpu_hours", e.get("requested_hours", 0)) or 0) for e in entries if (account is None or e["account_alias"] == account) and (phase is None or e["phase"] == phase))

def reserve_gpu_run(ledger_path, *, run_id, account_alias, phase, requested_hours, manifest_sha256, config_sha256) -> BudgetReservation:
    path = Path(ledger_path); data = _load(path); entries = data["entries"]
    if any(e["run_id"] == run_id for e in entries): raise DuplicateRun(run_id)
    if account_alias not in ACCOUNTS: raise BudgetError("unknown account alias")
    if phase not in PHASE_CAPS: raise BudgetError("unknown phase")
    if float(requested_hours) <= 0: raise BudgetError("requested hours must be positive")
    _hash(manifest_sha256, "manifest"); _hash(config_sha256, "config")
    request = float(requested_hours)
    if _hours(entries) + request > 60.0 + 1e-12: raise BudgetExceeded("aggregate budget exceeds 60 hours")
    if _hours(entries, account_alias) + request > 30.0 + 1e-12: raise AccountBudgetExceeded("account budget exceeds 30 hours")
    if _hours(entries, phase=phase) + request > PHASE_CAPS[phase] + 1e-12: raise PhaseBudgetExceeded(f"phase budget exceeds {PHASE_CAPS[phase]} hours")
    entry = {"run_id": run_id, "account_alias": account_alias, "phase": phase, "requested_gpu_hours": request, "actual_gpu_hours": None, "manifest_sha256": manifest_sha256, "config_sha256": config_sha256, "artefact_sha256": None, "status": "RESERVED"}
    entries.append(entry); _save(path, data)
    return BudgetReservation(run_id, account_alias, phase, request, manifest_sha256, config_sha256)

def complete_gpu_run(ledger_path, *, run_id, actual_gpu_hours, artefact_sha256) -> BudgetEntry:
    path = Path(ledger_path); data = _load(path)
    matches = [e for e in data["entries"] if e["run_id"] == run_id]
    if not matches: raise BudgetError("unknown run")
    entry = matches[0]
    if entry.get("status") != "RESERVED": raise BudgetError("run is not reserved")
    if float(actual_gpu_hours) < 0 or float(actual_gpu_hours) > float(entry["requested_gpu_hours"]): raise BudgetError("actual hours exceed reservation")
    _hash(artefact_sha256, "artefact")
    entry.update(actual_gpu_hours=float(actual_gpu_hours), artefact_sha256=artefact_sha256, status="COMPLETED")
    _save(path, data)
    return BudgetEntry(**entry)
