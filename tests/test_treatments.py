SAMPLE_SCHEDULE = {
    "type": "injection_protocol",
    "phases": [
        {"weeks": 6, "interval_days": 7, "dose": 1.0, "unit": "ml"},
        {"weeks": None, "interval_days": 14, "dose": 1.0, "unit": "ml"},
    ],
}


# --- Templates ---

def test_create_template(client):
    r = client.post("/api/treatment-templates/", json={
        "name": "B12 Standard",
        "category": "b12",
        "default_schedule": SAMPLE_SCHEDULE,
    })
    assert r.status_code == 201
    assert r.json()["name"] == "B12 Standard"


def test_get_template(client):
    r = client.post("/api/treatment-templates/", json={
        "name": "B12 Get Test",
        "category": "b12",
        "default_schedule": SAMPLE_SCHEDULE,
    })
    tid = r.json()["id"]
    r2 = client.get(f"/api/treatment-templates/{tid}")
    assert r2.status_code == 200
    assert r2.json()["category"] == "b12"


def test_get_template_404(client):
    assert client.get("/api/treatment-templates/99999").status_code == 404


def test_list_templates_filter_category(client):
    client.post("/api/treatment-templates/", json={
        "name": "Enzyme A",
        "category": "enzyme",
        "default_schedule": {"type": "daily"},
    })
    r = client.get("/api/treatment-templates/?category=enzyme")
    assert r.status_code == 200
    for item in r.json()["items"]:
        assert item["category"] == "enzyme"


def test_update_template(client):
    r = client.post("/api/treatment-templates/", json={
        "name": "Update Test",
        "category": "b12",
        "default_schedule": SAMPLE_SCHEDULE,
    })
    tid = r.json()["id"]
    r2 = client.patch(f"/api/treatment-templates/{tid}", json={"notes": "updated"})
    assert r2.status_code == 200
    assert r2.json()["notes"] == "updated"


def test_delete_template(client):
    r = client.post("/api/treatment-templates/", json={
        "name": "Delete Test",
        "category": "b12",
        "default_schedule": SAMPLE_SCHEDULE,
    })
    tid = r.json()["id"]
    assert client.delete(f"/api/treatment-templates/{tid}").status_code == 204
    assert client.get(f"/api/treatment-templates/{tid}").status_code == 404


# --- Protocols ---

def test_create_protocol(client):
    r = client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Fenja B12 Kur",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2026-01-01",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Fenja B12 Kur"
    assert data["active"] is True


def test_get_protocol_404(client):
    assert client.get("/api/treatment-protocols/99999").status_code == 404


def test_list_protocols_filter_active(client):
    client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Active Protocol",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2026-01-01",
        "active": True,
    })
    client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Archived Protocol",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2025-01-01",
        "active": False,
    })
    r = client.get("/api/treatment-protocols/?active=true")
    for item in r.json()["items"]:
        assert item["active"] is True


def test_update_protocol(client):
    r = client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Update Proto",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2026-01-01",
    })
    pid = r.json()["id"]
    r2 = client.patch(f"/api/treatment-protocols/{pid}", json={"active": False})
    assert r2.json()["active"] is False


def test_delete_protocol(client):
    r = client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Delete Proto",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2026-01-01",
    })
    pid = r.json()["id"]
    assert client.delete(f"/api/treatment-protocols/{pid}").status_code == 204


# --- Entries (nested under protocols) ---

def _create_protocol(client) -> int:
    r = client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Entry Test Proto",
        "schedule": SAMPLE_SCHEDULE,
        "start_date": "2026-01-01",
    })
    return r.json()["id"]


def test_create_entry(client):
    pid = _create_protocol(client)
    r = client.post(f"/api/treatment-protocols/{pid}/entries", json={
        "scheduled_date": "2026-01-07",
        "dose": 1.0,
        "unit": "ml",
    })
    assert r.status_code == 201
    assert r.json()["protocol_id"] == pid


def test_list_entries(client):
    pid = _create_protocol(client)
    client.post(f"/api/treatment-protocols/{pid}/entries", json={"scheduled_date": "2026-01-07"})
    client.post(f"/api/treatment-protocols/{pid}/entries", json={"scheduled_date": "2026-01-14"})
    r = client.get(f"/api/treatment-protocols/{pid}/entries")
    assert r.json()["total"] == 2


def test_treatment_entry_was_skipped(client):
    pid = _create_protocol(client)
    # Entry in the past with no administered_at → should be skipped
    r = client.post(f"/api/treatment-protocols/{pid}/entries", json={
        "scheduled_date": "2020-01-01",
    })
    assert r.status_code == 201
    assert r.json()["was_skipped"] is True


def test_entry_wrong_protocol_404(client):
    pid = _create_protocol(client)
    r = client.post(f"/api/treatment-protocols/{pid}/entries", json={"scheduled_date": "2026-01-07"})
    eid = r.json()["id"]
    assert client.get(f"/api/treatment-protocols/99999/entries/{eid}").status_code == 404


def test_update_entry(client):
    pid = _create_protocol(client)
    r = client.post(f"/api/treatment-protocols/{pid}/entries", json={"scheduled_date": "2026-01-07"})
    eid = r.json()["id"]
    r2 = client.patch(f"/api/treatment-protocols/{pid}/entries/{eid}", json={"notes": "done"})
    assert r2.json()["notes"] == "done"


def test_delete_entry(client):
    pid = _create_protocol(client)
    r = client.post(f"/api/treatment-protocols/{pid}/entries", json={"scheduled_date": "2026-01-07"})
    eid = r.json()["id"]
    assert client.delete(f"/api/treatment-protocols/{pid}/entries/{eid}").status_code == 204
