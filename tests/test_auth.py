import os


def test_missing_api_key_403(auth_client):
    r = auth_client.get("/api/health-markers/")
    assert r.status_code == 422 or r.status_code == 403


def test_wrong_api_key_403(auth_client):
    r = auth_client.get("/api/health-markers/", headers={"X-API-Key": "wrong-key"})
    assert r.status_code == 403


def test_correct_api_key(auth_client):
    api_key = os.environ.get("API_KEY", "dev-key-fenja-2026")
    r = auth_client.get("/api/health-markers/", headers={"X-API-Key": api_key})
    assert r.status_code == 200


def test_legacy_endpoints_unprotected(auth_client):
    assert auth_client.get("/").status_code == 200
    assert auth_client.get("/health").status_code == 200
