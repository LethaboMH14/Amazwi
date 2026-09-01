from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[1]


def test_kaggle_entrypoints_expose_help_without_side_effects():
    for name in ("reserve_run.py", "train_asr.py", "evaluate_asr.py", "package_run.py"):
        result = subprocess.run([sys.executable, str(ROOT / "kaggle" / name), "--help"], cwd=ROOT, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert "usage:" in result.stdout.lower()


def test_budget_json_declares_locked_allocations():
    import json
    data = json.loads((ROOT / "kaggle" / "budget.json").read_text(encoding="utf-8"))
    assert data["aggregate_cap_hours"] == 60
    assert data["account_cap_hours"] == 30
    assert data["phase_caps_hours"]["FIXED_TOURNAMENT"] == 8
