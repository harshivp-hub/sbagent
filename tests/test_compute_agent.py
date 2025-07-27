import json
import pytest
from orchestrator.orchestrator import Orchestrator

@pytest.mark.parametrize("fixture", ["over_provisioned","under_provisioned","mixed_workload"])
def test_agent(fixture, tmp_path):
    data = json.load(open(f"tests/fixtures/{fixture}.json"))
    orch = Orchestrator()
    result = orch.run(data)

    # Basic assertions
    assert isinstance(result.total_savings, float)
    assert isinstance(result.recommendations, list)

    # Save output for manual review if needed
    out_path = tmp_path / f"{fixture}_output.json"
    out_path.write_text(result.json(indent=2))
