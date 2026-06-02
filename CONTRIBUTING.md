# Contributing to NeuroEML

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/NeuroEML.git
cd NeuroEML
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest flake8 bandit
cp .env.example .env
# Fill in your API keys in .env
```

## Project Structure

```
NeuroEML/
├── config/           # Settings and configuration
├── parsers/          # .eml file parsing
├── engines/          # Analysis engines (identity, header, URL, AI, OSINT)
├── models/           # Main orchestrator
├── ui/               # Streamlit dashboard
├── tests/            # Test suite
├── docs/             # Documentation
└── samples/          # Sample .eml files for testing
```

## Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Run linter: `flake8 . --max-line-length=120`
6. Commit: `git commit -m "feat: describe your change"`
7. Push and open a Pull Request

## Commit Message Format

Use conventional commits:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `test:` — adding tests
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `chore:` — maintenance

## Areas for Contribution

- **New analysis engines** — e.g., attachment sandbox, ML classifiers
- **OSINT integrations** — Shodan, AlienVault OTX, URLhaus
- **Test coverage** — unit and integration tests for each engine
- **Documentation** — tutorials, usage examples
- **UI improvements** — new dashboard views, export formats
- **Performance** — caching, async I/O, batch processing

## Reporting Issues

When reporting bugs, please include:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
- Relevant log output (redact any sensitive data)

## Security Disclosures

For security vulnerabilities, please open a GitHub issue marked `[SECURITY]`.
Do **not** include real email samples with PII in issues or PRs.
