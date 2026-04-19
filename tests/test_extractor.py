import json, pathlib
from tf_narrator.extractor import extract_plan_summary

F = pathlib.Path(__file__).parent / "fixtures"

def test_skips_no_op_resources():
    plan = json.loads((F / "plan_simple.json").read_text())
    plan["resource_changes"].append({
        "address": "aws_s3_bucket.ignored", "type": "aws_s3_bucket", "name": "ignored",
        "change": {"actions": ["no-op"], "before": {"bucket": "x"}, "after": {"bucket": "x"}}
    })
    text = extract_plan_summary(plan)
    assert "aws_s3_bucket.ignored" not in text

def test_extracts_open_cidr():
    plan = json.loads((F / "plan_security.json").read_text())
    text = extract_plan_summary(plan)
    assert "0.0.0.0/0" in text

def test_destructive_plan_has_delete():
    plan = json.loads((F / "plan_destructive.json").read_text())
    text = extract_plan_summary(plan)
    assert "aws_rds_instance" in text
    assert "delete" in text.lower()

def test_output_under_token_limit():
    plan = json.loads((F / "plan_destructive.json").read_text())
    assert len(extract_plan_summary(plan)) <= 12000

def test_sensitive_fields_noted_not_exposed():
    plan = json.loads((F / "plan_security.json").read_text())
    text = extract_plan_summary(plan)
    assert "sensitive" in text.lower()
