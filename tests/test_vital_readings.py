def test_create_vital_reading(client):
    r = client.post("/api/vital-readings/", json={
        "marker_type": "heart_rate",
        "value": 80.0,
        "unit": "bpm",
        "source": "halsband",
    })
    assert r.status_code == 201
    assert r.json()["marker_type"] == "heart_rate"


def test_get_vital_reading(client):
    r = client.post("/api/vital-readings/", json={
        "marker_type": "weight",
        "value": 28.5,
        "unit": "kg",
        "source": "waage",
    })
    rid = r.json()["id"]
    r2 = client.get(f"/api/vital-readings/{rid}")
    assert r2.status_code == 200
    assert r2.json()["value"] == 28.5


def test_get_vital_reading_404(client):
    assert client.get("/api/vital-readings/99999").status_code == 404


def test_list_vital_readings_filter_marker_type(client):
    client.post("/api/vital-readings/", json={
        "marker_type": "temperature", "value": 38.5, "unit": "°C", "source": "manual",
    })
    client.post("/api/vital-readings/", json={
        "marker_type": "heart_rate", "value": 90, "unit": "bpm", "source": "halsband",
    })
    r = client.get("/api/vital-readings/?marker_type=temperature")
    for item in r.json()["items"]:
        assert item["marker_type"] == "temperature"


def test_list_vital_readings_filter_source(client):
    client.post("/api/vital-readings/", json={
        "marker_type": "weight", "value": 29.0, "unit": "kg", "source": "waage",
    })
    r = client.get("/api/vital-readings/?source=waage")
    for item in r.json()["items"]:
        assert item["source"] == "waage"


def test_update_vital_reading(client):
    r = client.post("/api/vital-readings/", json={
        "marker_type": "weight", "value": 28.0, "unit": "kg", "source": "waage",
    })
    rid = r.json()["id"]
    r2 = client.patch(f"/api/vital-readings/{rid}", json={"value": 28.5})
    assert r2.json()["value"] == 28.5


def test_delete_vital_reading(client):
    r = client.post("/api/vital-readings/", json={
        "marker_type": "weight", "value": 28.0, "unit": "kg", "source": "waage",
    })
    rid = r.json()["id"]
    assert client.delete(f"/api/vital-readings/{rid}").status_code == 204
    assert client.get(f"/api/vital-readings/{rid}").status_code == 404
