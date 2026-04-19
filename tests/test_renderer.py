import json
from tf_narrator.renderer import render_terminal, render_github, render_slack, render_json

SAMPLE = {
    "risk_score": "HIGH",
    "risk_reason": "Deletes the primary database",
    "summary": "This plan permanently deletes the RDS instance.",
    "changes": [
        {"action": "delete", "resource": "aws_rds_instance.primary",
         "explanation": "Deletes the production database.", "warnings": ["Data loss risk"]}
    ],
    "security_observations": ["SSH open to 0.0.0.0/0"],
    "action_required": ["Confirm you have a recent backup"],
    "looks_intentional": False,
}

def test_terminal_shows_risk():
    assert "HIGH" in render_terminal(SAMPLE, use_color=False)

def test_terminal_shows_resource():
    assert "aws_rds_instance.primary" in render_terminal(SAMPLE, use_color=False)

def test_terminal_shows_security_obs():
    assert "0.0.0.0/0" in render_terminal(SAMPLE, use_color=False)

def test_no_color_no_escape_codes():
    assert "\033[" not in render_terminal(SAMPLE, use_color=False)

def test_color_has_escape_codes():
    assert "\033[" in render_terminal(SAMPLE, use_color=True)

def test_github_is_markdown():
    out = render_github(SAMPLE)
    assert out.startswith("##") and "HIGH" in out

def test_json_is_valid():
    assert json.loads(render_json(SAMPLE))["risk_score"] == "HIGH"

def test_slack_contains_risk():
    assert "HIGH" in render_slack(SAMPLE)
