import json

from fastapi.testclient import TestClient

from fenja_health_dl.main import app
from fenja_health_dl.model import MODEL_PATH

client = TestClient(app)


def test_model_reload_changes_bias():
    # write new model state
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "w") as f:
        json.dump({"bias": 0.42}, f)

    # reload model
    r = client.post("/model/reload")
    assert r.status_code == 200
    assert r.json()["reloaded"] is True
    assert abs(r.json()["model"]["bias"] - 0.42) < 1e-9

    # prediction reflects new bias
    r2 = client.post(
        "/predict",
        json={"weight": 30.0, "age": 5, "activity": 6},
    )

    assert r2.status_code == 200

    expected = (5 + (10 - 6)) / 20 + 0.42
    assert abs(r2.json()["risk_score"] - expected) < 1e-9

