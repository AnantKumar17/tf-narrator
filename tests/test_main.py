import json, sys, pytest
from pathlib import Path
from unittest.mock import patch

F = Path(__file__).parent / "fixtures"

MOCK = {
    "risk_score": "LOW", "risk_reason": "Only creating non-critical resources",
    "summary": "Creates an S3 bucket with versioning.",
    "changes": [{"action": "create", "resource": "aws_s3_bucket.my_app_assets",
                 "explanation": "Creates a new S3 bucket.", "warnings": []}],
    "security_observations": [], "action_required": [], "looks_intentional": True,
}

@patch("tf_narrator.main.call_claude", return_value=MOCK)
def test_simple_plan_terminal(_, capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    p = tmp_path / "plan.json"
    p.write_text((F / "plan_simple.json").read_text())
    sys.argv = ["tf-narrator", str(p), "--no-color"]
    with pytest.raises(SystemExit) as e:
        from tf_narrator.main import main; main()
    assert e.value.code == 0
    out = capsys.readouterr().out
    assert "LOW" in out and "aws_s3_bucket" in out

@patch("tf_narrator.main.call_claude", return_value=MOCK)
def test_github_format(_, capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    p = tmp_path / "plan.json"
    p.write_text((F / "plan_simple.json").read_text())
    sys.argv = ["tf-narrator", str(p), "--format", "github"]
    with pytest.raises(SystemExit):
        from tf_narrator.main import main; main()
    assert capsys.readouterr().out.strip().startswith("##")

@patch("tf_narrator.main.call_claude", return_value=MOCK)
def test_json_format(_, capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    p = tmp_path / "plan.json"
    p.write_text((F / "plan_simple.json").read_text())
    sys.argv = ["tf-narrator", str(p), "--format", "json"]
    with pytest.raises(SystemExit):
        from tf_narrator.main import main; main()
    assert json.loads(capsys.readouterr().out)["risk_score"] == "LOW"

def test_missing_api_key_exits_1(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    p = tmp_path / "plan.json"
    p.write_text((F / "plan_simple.json").read_text())
    sys.argv = ["tf-narrator", str(p)]
    from tf_narrator.main import main
    with pytest.raises(SystemExit) as e: main()
    assert e.value.code == 1

def test_empty_input_exits_1(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    p = tmp_path / "empty.json"
    p.write_text("")
    sys.argv = ["tf-narrator", str(p)]
    from tf_narrator.main import main
    with pytest.raises(SystemExit) as e: main()
    assert e.value.code == 1
