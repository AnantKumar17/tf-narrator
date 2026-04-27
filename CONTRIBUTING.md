# Contributing to tf-narrator

👋 Want to contribute to tf-narrator?

This tool transforms Terraform plans into clear, risk-scored explanations. We welcome contributions that improve risk analysis, output clarity, or CI/CD integration.

## How to Contribute

### 1. Bug Reports & Feature Requests
- Check existing [issues](https://github.com/AnantKumar17/tf-narrator/issues) first
- For bugs: include Terraform version, sample plan JSON (sanitized!), and error output
- For features: explain the use case and why it improves Terraform workflows

### 2. Code Contributions

**We accept:**
- Small, focused patches that are easy to review manually
- Prompts you used to generate LLM-based changes (with evidence of manual testing)
- New output format handlers (e.g., Jira markdown, HTML)
- Improved risk scoring logic
- Documentation improvements

**Please avoid:**
- Large, unreviewed LLM-generated patches
- Changes without testing on real Terraform plans
- Breaking changes to CLI interface

### 3. Testing Requirements

All contributions must include evidence of testing:
- Test with at least 3 real Terraform plans (create, update, destroy scenarios)
- Show before/after output for changes
- Verify risk scoring is accurate
- Test all output formats if modifying output logic

## Development Setup

### Prerequisites
- Python 3.9+
- Terraform (for generating test plans)
- Anthropic API key

### Installation for Development

```bash
git clone https://github.com/AnantKumar17/tf-narrator.git
cd tf-narrator

# Install in development/editable mode
pip install -e ".[dev]"

# Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Running Tests

```bash
# Unit tests
pytest tests/ -v

# Linting
ruff check tf_narrator/

# Type checking (if applicable)
mypy tf_narrator/

# Generate a test plan for manual testing
cd tests/fixtures
terraform init
terraform plan -out=test.tfplan
terraform show -json test.tfplan > test.json
tf-narrator test.json
```

### Creating Test Fixtures

```bash
# Add new test plans to tests/fixtures/
# Sanitize sensitive data before committing!
terraform plan -out=new_scenario.tfplan
terraform show -json new_scenario.tfplan > tests/fixtures/new_scenario.json

# Remove sensitive values
# Edit tests/fixtures/new_scenario.json and replace:
# - Account IDs → "123456789012"
# - Secrets/keys → "REDACTED"
# - Internal IPs → "10.0.0.0"
```

## Contribution Guidelines

### Code Style
- **Python**: Follow PEP 8, use type hints
- Keep functions focused and well-documented
- Add docstrings for public functions
- Use f-strings for formatting

### Commit Messages
- Use present tense ("Add risk scoring logic" not "Added risk scoring logic")
- Keep first line under 70 characters
- Reference issue numbers when applicable

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear commits
4. Add tests for new functionality
5. Run the test suite: `pytest tests/ -v`
6. Update documentation if needed
7. Submit PR with:
   - Clear description of what changed and why
   - Evidence of testing (sample outputs)
   - If LLM-generated: include the prompts used

### What to Include in Your PR

- **Description**: What problem does this solve? What's the approach?
- **Testing evidence**: Show tf-narrator output on sample plans
- **Risk scoring impact**: If changing scoring logic, show before/after risk levels
- **Breaking changes**: Clearly mark if CLI interface changed
- **Documentation**: Update README.md if user-facing changes

## Areas We Need Help With

Check the [issues page](https://github.com/AnantKumar17/tf-narrator/issues) for backlog. High-priority areas:

### Risk Scoring Improvements
- Better detection of security issues (open security groups, public S3 buckets)
- Compliance pattern detection (GDPR, HIPAA, SOC2)
- Cost impact estimation
- Blast radius calculation (how many resources affected)

### Output Formats
- HTML output with collapsible sections
- Jira markdown format
- Microsoft Teams cards
- Custom template support

### Terraform Features
- Support for Terraform text output (not just JSON)
- Diff comparison between two plans
- Plan archiving and comparison
- Detect drift from known-good state

### Prompt Improvements
- Better Claude prompts for risk analysis
- More accurate "looks intentional" detection
- Better security observation quality
- Context-aware explanations (e.g., explain VPC concepts when analyzing networking)

### CI/CD Integration
- GitLab CI template
- Azure DevOps pipeline template
- Atlantis integration
- Pre-commit hook examples

## Risk Scoring Guidelines

When modifying risk scoring logic:

1. **Be conservative**: Better to over-flag than under-flag
2. **Consider context**: Same change can be LOW or HIGH risk depending on resource type
3. **Explain reasoning**: Risk reason should clearly state WHY it's that level
4. **Test diverse plans**: Different providers, resource types, and actions

### Risk Level Matrix

| Level | Description | Examples |
|-------|-------------|----------|
| **LOW** | Cosmetic changes, additive | Tags, labels, scaling up |
| **MEDIUM** | New infrastructure, config changes | New resources, network rules |
| **HIGH** | Destructive, security-sensitive | Destroy with data, IAM changes, public access |
| **CRITICAL** | Multi-resource destroy, data loss | RG deletion, account-level changes |

## Prompt Engineering Guidelines

When modifying the Claude prompt (`tf_narrator/prompts.py`):

1. **Be specific**: Ask for exact JSON structure
2. **Provide examples**: Show Claude what good output looks like
3. **Define risk levels**: Clearly explain LOW/MEDIUM/HIGH/CRITICAL
4. **Test token usage**: Keep prompts concise (target <2000 tokens)
5. **Handle edge cases**: Empty plans, no changes, errors

## Questions?

- Open an issue for discussion before starting major work
- For quick questions, comment on related issues
- Be respectful and constructive

## Security

- **Never commit real Terraform plans with sensitive data**
- Sanitize all test fixtures (account IDs, secrets, IPs)
- Be careful when posting error messages (may contain resource names)
- Review what data is sent to Claude API

## License

By contributing, you agree that your contributions will be licensed under the MIT License that covers this project.

---

**Note for AI-assisted development**: If you use LLM tools to generate code:
1. Review and understand all generated code before submitting
2. Test with real Terraform plans — AI can miss provider-specific nuances
3. Mention AI assistance in your PR description
4. Include the prompts you used for transparency
5. Manually verify risk scoring is accurate (don't trust LLM-generated risk levels)

**Remember**: This tool explains infrastructure changes. Make sure your contributions maintain clarity and accuracy.
