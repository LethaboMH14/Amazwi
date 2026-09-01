import json
import pytest
from amazwi_ml.budget import AccountBudgetExceeded, BudgetExceeded, reserve_gpu_run, complete_gpu_run


def seeded_ledger(tmp_path, **overrides):
    path = tmp_path / "ledger.json"
    data = {"version": 1, "entries": []}
    for key, hours in overrides.items():
        status = "COMPLETED" if key.startswith("completed") else "RESERVED"
        data["entries"].append({"run_id": key, "account_alias": "team-sonar-a", "phase": "ISIZULU_ADAPTATION", "requested_gpu_hours": hours, "actual_gpu_hours": hours if status == "COMPLETED" else None, "status": status, "manifest_sha256": "a" * 64, "config_sha256": "b" * 64, "artefact_sha256": "c" * 64})
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_aggregate_budget_cannot_exceed_sixty_hours(tmp_path):
    ledger = seeded_ledger(tmp_path, completed_a=30, completed_b=29)
    with pytest.raises(BudgetExceeded):
        reserve_gpu_run(ledger, run_id="run-60", account_alias="team-sonar-b", phase="REPRODUCIBILITY", requested_hours=2, manifest_sha256="a" * 64, config_sha256="b" * 64)


def test_each_account_is_capped_at_thirty_hours(tmp_path):
    ledger = seeded_ledger(tmp_path, reserved_a=29.5)
    with pytest.raises(AccountBudgetExceeded):
        reserve_gpu_run(ledger, run_id="run-a", account_alias="team-sonar-a", phase="ISIZULU_ADAPTATION", requested_hours=1, manifest_sha256="a" * 64, config_sha256="b" * 64)


def test_reservation_then_completion_is_deterministic(tmp_path):
    ledger = tmp_path / "ledger.json"
    reservation = reserve_gpu_run(ledger, run_id="run-1", account_alias="team-sonar-a", phase="FIXED_TOURNAMENT", requested_hours=1, manifest_sha256="a" * 64, config_sha256="b" * 64)
    entry = complete_gpu_run(ledger, run_id="run-1", actual_gpu_hours=0.5, artefact_sha256="c" * 64)
    assert reservation.run_id == entry.run_id == "run-1"
    assert json.loads(ledger.read_text())["entries"][0]["status"] == "COMPLETED"
