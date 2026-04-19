import json


def render_terminal(result: dict, use_color: bool = True) -> str:
    risk = result.get("risk_score", "UNKNOWN")

    # ANSI colors
    colors = {
        "LOW": "\033[32m" if use_color else "",
        "MEDIUM": "\033[33m" if use_color else "",
        "HIGH": "\033[31m" if use_color else "",
        "CRITICAL": "\033[35m" if use_color else "",
        "RESET": "\033[0m" if use_color else "",
        "BOLD": "\033[1m" if use_color else "",
    }

    risk_color = colors.get(risk, "")
    reset = colors["RESET"]
    bold = colors["BOLD"]

    lines = []

    # Header
    lines.append(f"\n{bold}{'=' * 70}{reset}")
    lines.append(f"{bold}Terraform Plan Analysis{reset}")
    lines.append(f"{bold}{'=' * 70}{reset}")
    lines.append(f"{bold}Risk Level:{reset} {risk_color}{risk}{reset}")
    lines.append(f"{bold}Reason:{reset} {result.get('risk_reason', 'N/A')}")

    change_counts = {}
    for change in result.get("changes", []):
        action = change.get("action", "unknown")
        change_counts[action] = change_counts.get(action, 0) + 1

    if change_counts:
        counts_str = ", ".join([f"{k}: {v}" for k, v in sorted(change_counts.items())])
        lines.append(f"{bold}Changes:{reset} {counts_str}")

    lines.append(f"{bold}{'=' * 70}{reset}\n")

    # Summary
    lines.append(f"{bold}Summary:{reset}")
    lines.append(result.get("summary", "No summary provided"))
    lines.append("")

    # Changes
    if changes := result.get("changes", []):
        lines.append(f"{bold}Changes:{reset}")
        action_symbols = {
            "create": "[+]",
            "update": "[~]",
            "delete": "[-]",
            "replace": "[±]",
        }

        for change in changes:
            action = change.get("action", "unknown")
            symbol = action_symbols.get(action, "[?]")
            resource = change.get("resource", "unknown")
            explanation = change.get("explanation", "No explanation")

            lines.append(f"\n  {symbol} {bold}{resource}{reset}")
            lines.append(f"      {explanation}")

            if warnings := change.get("warnings", []):
                for warning in warnings:
                    lines.append(f"      {risk_color}Warning:{reset} {warning}")
        lines.append("")

    # Security observations
    if security_obs := result.get("security_observations", []):
        lines.append(f"{bold}Security Observations:{reset}")
        for obs in security_obs:
            lines.append(f"  - {obs}")
        lines.append("")

    # Action required
    if actions := result.get("action_required", []):
        lines.append(f"{bold}Action Required:{reset}")
        for action in actions:
            lines.append(f"  - {action}")
        lines.append("")

    # Intentionality
    intentional = result.get("looks_intentional", True)
    intentional_str = "Yes" if intentional else "No"
    lines.append(f"{bold}Looks Intentional:{reset} {intentional_str}")
    lines.append("")

    return "\n".join(lines)


def render_github(result: dict) -> str:
    risk = result.get("risk_score", "UNKNOWN")
    risk_emoji = {
        "LOW": ":green_circle:",
        "MEDIUM": ":yellow_circle:",
        "HIGH": ":red_circle:",
        "CRITICAL": ":purple_circle:",
    }

    lines = []
    lines.append(f"## {risk_emoji.get(risk, ':white_circle:')} Terraform Plan Analysis - {risk}")
    lines.append("")
    lines.append(f"**Risk Reason:** {result.get('risk_reason', 'N/A')}")
    lines.append("")

    # Summary
    lines.append("### Summary")
    lines.append(result.get("summary", "No summary provided"))
    lines.append("")

    # Changes
    if changes := result.get("changes", []):
        lines.append("### Changes")
        for change in changes:
            action = change.get("action", "unknown")
            resource = change.get("resource", "unknown")
            explanation = change.get("explanation", "No explanation")

            action_emoji = {
                "create": ":heavy_plus_sign:",
                "update": ":recycle:",
                "delete": ":heavy_minus_sign:",
                "replace": ":arrows_counterclockwise:",
            }

            lines.append(f"#### {action_emoji.get(action, ':question:')} {resource}")
            lines.append(f"**Action:** {action}")
            lines.append(f"{explanation}")

            if warnings := change.get("warnings", []):
                lines.append("**Warnings:**")
                for warning in warnings:
                    lines.append(f"- {warning}")
            lines.append("")

    # Security observations
    if security_obs := result.get("security_observations", []):
        lines.append("### Security Observations")
        for obs in security_obs:
            lines.append(f"- {obs}")
        lines.append("")

    # Action required
    if actions := result.get("action_required", []):
        lines.append("### Action Required")
        for action in actions:
            lines.append(f"- {action}")
        lines.append("")

    # Intentionality
    intentional = result.get("looks_intentional", True)
    intentional_str = "Yes" if intentional else "No"
    lines.append(f"**Looks Intentional:** {intentional_str}")

    return "\n".join(lines)


def render_slack(result: dict) -> str:
    risk = result.get("risk_score", "UNKNOWN")

    lines = []
    lines.append(f"*Terraform Plan Analysis - {risk}*")
    lines.append(f"*Risk Reason:* {result.get('risk_reason', 'N/A')}")
    lines.append("")

    # Summary
    lines.append("*Summary*")
    lines.append(result.get("summary", "No summary provided"))
    lines.append("")

    # Changes
    if changes := result.get("changes", []):
        lines.append("*Changes*")
        for change in changes:
            action = change.get("action", "unknown")
            resource = change.get("resource", "unknown")
            explanation = change.get("explanation", "No explanation")

            lines.append(f"• `{resource}` ({action})")
            lines.append(f"  {explanation}")

            if warnings := change.get("warnings", []):
                for warning in warnings:
                    lines.append(f"  :warning: {warning}")
        lines.append("")

    # Security observations
    if security_obs := result.get("security_observations", []):
        lines.append("*Security Observations*")
        for obs in security_obs:
            lines.append(f"• {obs}")
        lines.append("")

    # Action required
    if actions := result.get("action_required", []):
        lines.append("*Action Required*")
        for action in actions:
            lines.append(f"• {action}")
        lines.append("")

    # Intentionality
    intentional = result.get("looks_intentional", True)
    intentional_str = "Yes" if intentional else "No"
    lines.append(f"*Looks Intentional:* {intentional_str}")

    return "\n".join(lines)


def render_json(result: dict) -> str:
    return json.dumps(result, indent=2)
