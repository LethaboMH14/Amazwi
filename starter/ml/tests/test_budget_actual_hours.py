import json

from amazwi_ml.budget import reserve_gpu_run


def test_completed_runs_consume_actual_not_reserved_hours(tmp_path):
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps({"version": 1, "entries": [{
        "run_id": "old", "account_alias": "team-sonar-a", "phase": "FIXED_TOURNAMENT",
        "requested_hours": 8, "actual_gpu_hours": 1, "status": "COMPLETED",
        "manifest_sha256": "a" * 64, "config_sha256": "b" * 64,
    }]}), encoding="utf-8")
    reservation = reserve_gpu_run(ledger, run_id="new", account_alias="team-sonar-b", phase="FIXED_TOURNAMENT", requested_hours=7, manifest_sha256="a" * 64, config_sha256="b" * 64)
    assert reservation.requested_gpu_hours == 7
