import json
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    # Repo root is two levels up from tests/contracts
    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / "Docs" / "2-Design-Concept" / "0-Factory-Saas" / "contracts-examples"


def load_json(fixtures_dir: Path, name: str):
    p = fixtures_dir / name
    with p.open() as f:
        return json.load(f)


@pytest.fixture(scope="session")
def plan_matrix(fixtures_dir):
    return load_json(fixtures_dir, "plan_matrix_example.json")


@pytest.fixture(scope="session")
def product_detail(fixtures_dir):
    return load_json(fixtures_dir, "product_detail_example.json")


@pytest.fixture(scope="session")
def price_snapshot(fixtures_dir):
    return load_json(fixtures_dir, "price_snapshot_example.json")


@pytest.fixture(scope="session")
def order_line(fixtures_dir):
    return load_json(fixtures_dir, "order_line_example.json")


@pytest.fixture(scope="session")
def outbox_event(fixtures_dir):
    return load_json(fixtures_dir, "outbox_event_example.json")


@pytest.fixture(scope="session")
def telemetry_event(fixtures_dir):
    return load_json(fixtures_dir, "telemetry_event_example.json")
