import uuid


def unique_date():
    """Generate a unique date to avoid unique constraint conflicts across tests."""
    import random
    return f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"


def test_create_daily_log(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-01", "energy_level": 4, "stool_consistency": 2})
    assert r.status_code == 201
    data = r.json()
    assert data["date"] == "2026-03-01"
    assert data["energy_level"] == 4


def test_get_daily_log(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-02"})
    log_id = r.json()["id"]
    r2 = client.get(f"/api/daily-logs/{log_id}")
    assert r2.status_code == 200
    assert r2.json()["date"] == "2026-03-02"


def test_get_daily_log_404(client):
    assert client.get("/api/daily-logs/99999").status_code == 404


def test_daily_log_appetite_ratio_computed(client):
    r = client.post("/api/daily-logs/", json={
        "date": "2026-03-03",
        "food_offered_g": 400,
        "food_eaten_g": 300,
    })
    assert r.status_code == 201
    assert r.json()["appetite_ratio"] == 0.75


def test_list_daily_logs_with_filter(client):
    client.post("/api/daily-logs/", json={"date": "2026-01-10"})
    client.post("/api/daily-logs/", json={"date": "2026-06-10"})
    r = client.get("/api/daily-logs/?from_date=2026-05-01")
    for item in r.json()["items"]:
        assert item["date"] >= "2026-05-01"


def test_update_daily_log(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-04"})
    log_id = r.json()["id"]
    r2 = client.patch(f"/api/daily-logs/{log_id}", json={"energy_level": 5})
    assert r2.status_code == 200
    assert r2.json()["energy_level"] == 5


def test_delete_daily_log(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-05"})
    log_id = r.json()["id"]
    assert client.delete(f"/api/daily-logs/{log_id}").status_code == 204
    assert client.get(f"/api/daily-logs/{log_id}").status_code == 404


def test_daily_log_duplicate_date_409(client):
    client.post("/api/daily-logs/", json={"date": "2026-02-20"})
    r = client.post("/api/daily-logs/", json={"date": "2026-02-20"})
    assert r.status_code == 409


def test_daily_log_validation_stool_out_of_range(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-06", "stool_consistency": 10})
    assert r.status_code == 422


def test_daily_log_validation_pain_out_of_range(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-03-07", "pain_score": 30})
    assert r.status_code == 422


# --- Observation tests ---

def test_create_observation(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-04-01"})
    log_id = r.json()["id"]
    r2 = client.post(f"/api/daily-logs/{log_id}/observations", json={
        "symptom_type": "niesen",
        "value_bool": True,
        "notes": "morgens",
    })
    assert r2.status_code == 201
    assert r2.json()["symptom_type"] == "niesen"
    assert r2.json()["daily_log_id"] == log_id


def test_list_observations(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-04-02"})
    log_id = r.json()["id"]
    client.post(f"/api/daily-logs/{log_id}/observations", json={"symptom_type": "zittern", "value_bool": True})
    client.post(f"/api/daily-logs/{log_id}/observations", json={"symptom_type": "husten", "value_numeric": 3})
    r2 = client.get(f"/api/daily-logs/{log_id}/observations")
    assert r2.json()["total"] == 2


def test_observation_wrong_log_404(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-04-03"})
    log_id = r.json()["id"]
    r2 = client.post(f"/api/daily-logs/{log_id}/observations", json={"symptom_type": "test", "value_bool": True})
    obs_id = r2.json()["id"]
    # Try accessing with wrong log_id
    r3 = client.get(f"/api/daily-logs/99999/observations/{obs_id}")
    assert r3.status_code == 404


def test_update_observation(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-04-04"})
    log_id = r.json()["id"]
    r2 = client.post(f"/api/daily-logs/{log_id}/observations", json={"symptom_type": "test", "value_bool": True})
    obs_id = r2.json()["id"]
    r3 = client.patch(f"/api/daily-logs/{log_id}/observations/{obs_id}", json={"notes": "updated"})
    assert r3.status_code == 200
    assert r3.json()["notes"] == "updated"


def test_delete_observation(client):
    r = client.post("/api/daily-logs/", json={"date": "2026-04-05"})
    log_id = r.json()["id"]
    r2 = client.post(f"/api/daily-logs/{log_id}/observations", json={"symptom_type": "test", "value_bool": True})
    obs_id = r2.json()["id"]
    assert client.delete(f"/api/daily-logs/{log_id}/observations/{obs_id}").status_code == 204
