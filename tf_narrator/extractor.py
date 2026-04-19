import json

INTERESTING_KEYS = [
    "instance_type", "engine", "engine_version", "ingress", "egress",
    "bucket", "acl", "policy", "role", "runtime", "handler", "desired_count",
    "image", "port_mappings", "publicly_accessible", "cidr_blocks",
    "from_port", "to_port", "type",
]

def extract_plan_summary(plan_data: dict) -> str:
    lines = []

    if tv := plan_data.get("terraform_version"):
        lines.append(f"Terraform version: {tv}\n")

    resource_changes = plan_data.get("resource_changes", [])
    if not resource_changes:
        return json.dumps(plan_data)[:8000]

    for change in resource_changes:
        actions = change.get("change", {}).get("actions", [])
        if actions == ["no-op"]:
            continue

        address = change.get("address", "unknown")
        resource_type = change.get("type", "")
        action_str = " + ".join(actions)
        before = change.get("change", {}).get("before") or {}
        after  = change.get("change", {}).get("after") or {}

        lines.append(f"Resource: {address} ({resource_type})")
        lines.append(f"Action: {action_str}")

        for key in INTERESTING_KEYS:
            if key in after:
                lines.append(f"  {key}: {json.dumps(after[key])[:300]}")
            elif key in before:
                lines.append(f"  {key} (before): {json.dumps(before[key])[:300]}")

        after_sensitive = change.get("change", {}).get("after_sensitive") or {}
        sensitive_keys = [k for k, v in after_sensitive.items() if v]
        if sensitive_keys:
            lines.append(f"  [sensitive fields present: {', '.join(sensitive_keys)}]")

        lines.append("")

    return "\n".join(lines)[:12000]
