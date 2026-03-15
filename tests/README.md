Contract tests for Factory-SaaS

Run these checks locally to validate contract fixtures and basic schema invariants.

Setup (recommended in virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q tests/contracts
```

The tests validate JSON fixtures in `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/`.
