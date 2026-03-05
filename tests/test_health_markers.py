def test_create_health_marker(client):
    r = client.post("/api/health-markers/", json={"weight_kg": 28.5, "cobalamin_b12": 250})
    assert r.status_code == 201
    data = r.json()
    assert data["weight_kg"] == 28.5
    assert data["cobalamin_b12"] == 250
    assert "id" in data
    assert "timestamp" in data


def test_get_health_marker(client):
    r = client.post("/api/health-markers/", json={"weight_kg": 30.0})
    marker_id = r.json()["id"]
    r2 = client.get(f"/api/health-markers/{marker_id}")
    assert r2.status_code == 200
    assert r2.json()["weight_kg"] == 30.0


def test_get_health_marker_404(client):
    r = client.get("/api/health-markers/99999")
    assert r.status_code == 404


def test_list_health_markers(client):
    client.post("/api/health-markers/", json={"weight_kg": 28.0})
    client.post("/api/health-markers/", json={"weight_kg": 29.0})
    r = client.get("/api/health-markers/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 2
    assert "items" in data
    assert "pages" in data


def test_list_health_markers_pagination(client):
    for i in range(5):
        client.post("/api/health-markers/", json={"weight_kg": 25.0 + i})
    r = client.get("/api/health-markers/?page=1&page_size=2")
    data = r.json()
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_list_health_markers_filter_date(client):
    client.post("/api/health-markers/", json={"weight_kg": 28.0, "timestamp": "2026-01-01T00:00:00Z"})
    client.post("/api/health-markers/", json={"weight_kg": 29.0, "timestamp": "2026-06-01T00:00:00Z"})
    r = client.get("/api/health-markers/?from_date=2026-05-01T00:00:00Z")
    data = r.json()
    for item in data["items"]:
        assert item["timestamp"] >= "2026-05-01"


def test_update_health_marker(client):
    r = client.post("/api/health-markers/", json={"weight_kg": 28.0})
    marker_id = r.json()["id"]
    r2 = client.patch(f"/api/health-markers/{marker_id}", json={"weight_kg": 29.5})
    assert r2.status_code == 200
    assert r2.json()["weight_kg"] == 29.5


def test_delete_health_marker(client):
    r = client.post("/api/health-markers/", json={"weight_kg": 28.0})
    marker_id = r.json()["id"]
    r2 = client.delete(f"/api/health-markers/{marker_id}")
    assert r2.status_code == 204
    r3 = client.get(f"/api/health-markers/{marker_id}")
    assert r3.status_code == 404
