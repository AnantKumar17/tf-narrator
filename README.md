# tf-narrator

A command-line tool that transforms Terraform plan JSON output into clear, plain-English explanations with risk scoring, security observations, and actionable insights. Powered by Claude AI.

## Features

- Plain English explanations of Terraform plans
- Risk scoring (LOW, MEDIUM, HIGH, CRITICAL)
- Security observations and warnings
- Action-required checklist before applying
- Multiple output formats: terminal (colored), GitHub markdown, Slack, JSON
- Reads from stdin or file
- No dependencies on Terraform state or configuration files

## Requirements

- Python 3.9 or higher
- An [Anthropic API key](https://console.anthropic.com/)

## Installation

```bash
pip install git+https://github.com/AnantKumar17/tf-narrator.git
```

Install a specific version:

```bash
pip install git+https://github.com/AnantKumar17/tf-narrator.git@v1.0.0
```

## Setup

Get an API key from [console.anthropic.com](https://console.anthropic.com/) and export it:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

To persist it, add that line to your `~/.zshrc` or `~/.bashrc` and run `source ~/.zshrc`.

On Windows (PowerShell):

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

## Quick Start

After installing and setting the API key:

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
tf-narrator plan.json
```

Or pipe directly:

```bash
terraform show -json plan.tfplan | tf-narrator
```

## Usage

### Output formats

```bash
tf-narrator plan.json                      # colored terminal (default)
tf-narrator plan.json --no-color           # terminal, no ANSI colors
tf-narrator plan.json --format github      # GitHub-flavored markdown
tf-narrator plan.json --format slack       # Slack markdown
tf-narrator plan.json --format json        # raw JSON
```

### Use a different Claude model

```bash
tf-narrator plan.json --model claude-opus-4-20250514
```

## Example Output

```
======================================================================
Terraform Plan Analysis
======================================================================
Risk Level: MEDIUM
Reason: Creates new infrastructure with storage access keys and role assignments that need security review
Changes: create: 7
======================================================================

Summary:
This plan creates a complete healthcare diagnosis workflow infrastructure including 
a resource group, storage account with container, lifecycle policies, and role-based 
access controls. All resources are net-new creations with no existing infrastructure 
being modified or destroyed.

Changes:

  [+] module.hc_diagnosis_wf.azurerm_resource_group.hc_diagnosis_wf_rg
      Creates a new Azure resource group to contain all the healthcare diagnosis 
      workflow resources

  [+] module.hc_diagnosis_wf.azurerm_storage_account.hc_diagnosis_wf_storage
      Creates a new storage account for healthcare diagnosis data with sensitive 
      connection strings and access keys
      Warning: Contains sensitive authentication keys that will be stored in state file
      Warning: Ensure encryption and network restrictions are properly configured

Security Observations:
  - Storage account contains sensitive access keys and connection strings
  - Healthcare data requires special compliance considerations (HIPAA, GDPR, etc.)
  - Role assignments grant access to diagnosis workflow data - verify principals

Action Required:
  - Verify role assignment principals are correct and follow least privilege
  - Confirm storage account has appropriate security configurations
  - Ensure compliance requirements for healthcare data are met

Looks Intentional: Yes
```

### All options

```
usage: tf-narrator [-h] [--format {terminal,github,slack,json}] [--no-color]
                   [--model MODEL] [--version]
                   [plan_file]

positional arguments:
  plan_file             Plan JSON file (reads stdin if omitted)

options:
  -h, --help            show this help message and exit
  --format              Output format (default: terminal)
  --no-color            Disable ANSI colors in terminal output
  --model               Claude model to use (default: claude-sonnet-4-20250514)
  --version             Show version and exit
```

## CI/CD Integration

### GitHub Actions

Add `ANTHROPIC_API_KEY` as a repository secret, then:

```yaml
- name: Generate plan JSON
  run: |
    terraform plan -out=plan.tfplan
    terraform show -json plan.tfplan > plan.json

- name: Analyze with tf-narrator
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    pip install git+https://github.com/AnantKumar17/tf-narrator.git
    tf-narrator plan.json --format github >> $GITHUB_STEP_SUMMARY
```

### Pre-apply hook

```bash
#!/bin/bash
# Save as .git/hooks/pre-apply or similar
terraform show -json plan.tfplan | tf-narrator

read -p "Proceed with terraform apply? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi
```

### Slack notification

```bash
terraform show -json plan.tfplan | \
  tf-narrator --format slack | \
  curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"'"$(cat)"'"}' \
    YOUR_SLACK_WEBHOOK_URL
```

## How It Works

1. Extracts relevant information from Terraform plan JSON (resource changes, actions, configuration)
2. Sends condensed plan summary to Claude AI for analysis
3. Claude returns structured JSON with risk assessment, explanations, and recommendations
4. tf-narrator formats the output in your chosen format

The tool is optimized to stay within API token limits while preserving important details about infrastructure changes, security configurations, and resource relationships.

## Updating

```bash
pip install --upgrade git+https://github.com/AnantKumar17/tf-narrator.git
```

## Uninstalling

```bash
pip uninstall tf-narrator
```

## Troubleshooting

**`command not found: tf-narrator`**
The Python scripts directory is not on your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**`Error: ANTHROPIC_API_KEY environment variable not set`**
Export the variable as shown in the Setup section.

**`ModuleNotFoundError: No module named 'anthropic'`**
Reinstall: `pip install --upgrade git+https://github.com/AnantKumar17/tf-narrator.git`

**Installation fails with "No module named 'setuptools'"**
```bash
pip install --upgrade pip setuptools wheel
```

## Development

```bash
git clone https://github.com/AnantKumar17/tf-narrator.git
cd tf-narrator
pip install -e ".[dev]"
pytest tests/ -v
ruff check tf_narrator/
```

## Contributing

Issues and pull requests are welcome at [github.com/AnantKumar17/tf-narrator](https://github.com/AnantKumar17/tf-narrator).

## License

MIT — see [LICENSE](LICENSE).

## Security

This tool sends Terraform plan data to the Claude API. Ensure you:
- Review what data is being sent (use `--format json` to see the extracted summary)
- Comply with your organization's data handling and security policies
- Never commit API keys to version control

## Roadmap

- Support for Terraform plan text output (not just JSON)
- Diff comparison between two plans
- Custom prompt templates
- Cache frequently analyzed plans
- Support for OpenTofu
