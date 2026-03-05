def test_create_vet_visit(client):
    r = client.post("/api/vet-visits/", json={"reason": "EPI Kontrolle"})
    assert r.status_code == 201
    assert r.json()["reason"] == "EPI Kontrolle"


def test_get_vet_visit(client):
    r = client.post("/api/vet-visits/", json={"reason": "Blutbild"})
    vid = r.json()["id"]
    r2 = client.get(f"/api/vet-visits/{vid}")
    assert r2.status_code == 200
    assert r2.json()["reason"] == "Blutbild"
    assert "protocols" in r2.json()


def test_get_vet_visit_404(client):
    assert client.get("/api/vet-visits/99999").status_code == 404


def test_list_vet_visits(client):
    client.post("/api/vet-visits/", json={"reason": "Kontrolle 1"})
    client.post("/api/vet-visits/", json={"reason": "Kontrolle 2"})
    r = client.get("/api/vet-visits/")
    assert r.status_code == 200
    assert r.json()["total"] >= 2


def test_update_vet_visit(client):
    r = client.post("/api/vet-visits/", json={"reason": "Update Test"})
    vid = r.json()["id"]
    r2 = client.patch(f"/api/vet-visits/{vid}", json={"diagnosis": "EPI bestätigt"})
    assert r2.status_code == 200
    assert r2.json()["diagnosis"] == "EPI bestätigt"


def test_delete_vet_visit(client):
    r = client.post("/api/vet-visits/", json={"reason": "Delete Test"})
    vid = r.json()["id"]
    assert client.delete(f"/api/vet-visits/{vid}").status_code == 204
    assert client.get(f"/api/vet-visits/{vid}").status_code == 404


def test_list_vet_visits_filter_date(client):
    client.post("/api/vet-visits/", json={"reason": "Alt", "timestamp": "2025-01-01T00:00:00Z"})
    client.post("/api/vet-visits/", json={"reason": "Neu", "timestamp": "2026-06-01T00:00:00Z"})
    r = client.get("/api/vet-visits/?from_date=2026-05-01T00:00:00Z")
    for item in r.json()["items"]:
        assert item["timestamp"] >= "2026-05-01"
