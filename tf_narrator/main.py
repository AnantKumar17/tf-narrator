import sys
import json
import os
import re
import anthropic
from .extractor import extract_plan_summary
from .renderer import render_terminal, render_github, render_slack, render_json
from .prompts import SYSTEM_PROMPT, build_user_prompt

__version__ = "1.0.0"

def call_claude(plan_text: str, model: str) -> dict:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(plan_text)}]
    )
    raw = message.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="tf-narrator",
        description="Explain Terraform plans in plain English using Claude"
    )
    parser.add_argument("plan_file", nargs="?", help="Plan JSON file (default: stdin)")
    parser.add_argument("--format", default="terminal",
                        choices=["terminal", "github", "slack", "json"])
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--model", default="claude-sonnet-4-20250514")
    parser.add_argument("--version", action="version", version=f"tf-narrator {__version__}")
    args = parser.parse_args()

    if args.plan_file:
        with open(args.plan_file) as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        print("Error: no plan data provided.", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        plan_data = json.loads(raw)
    except json.JSONDecodeError:
        plan_data = {"raw_output": raw}

    print("Analysing plan...", file=sys.stderr)
    plan_text = extract_plan_summary(plan_data)
    result = call_claude(plan_text, model=args.model)

    renderers = {
        "terminal": lambda: render_terminal(result, use_color=not args.no_color),
        "github":   lambda: render_github(result),
        "slack":    lambda: render_slack(result),
        "json":     lambda: render_json(result),
    }
    print(renderers[args.format]())
    sys.exit(0)

if __name__ == "__main__":
    main()
