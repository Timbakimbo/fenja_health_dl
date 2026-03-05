def test_weight_trend_combines_sources(client):
    # HealthMarker weight
    client.post("/api/health-markers/", json={"weight_kg": 28.0, "timestamp": "2026-01-01T00:00:00Z"})
    # VitalReading weight
    client.post("/api/vital-readings/", json={
        "marker_type": "weight", "value": 29.0, "unit": "kg", "source": "waage",
        "timestamp": "2026-01-15T00:00:00Z",
    })
    r = client.get("/api/insights/weight-trend")
    assert r.status_code == 200
    data = r.json()
    sources = {p["source"] for p in data}
    assert "health_marker" in sources
    assert "vital_reading" in sources
    # Should be sorted by timestamp
    timestamps = [p["timestamp"] for p in data]
    assert timestamps == sorted(timestamps)


def test_b12_trend(client):
    client.post("/api/health-markers/", json={"cobalamin_b12": 200, "timestamp": "2026-01-01T00:00:00Z"})
    client.post("/api/health-markers/", json={"cobalamin_b12": 350, "timestamp": "2026-02-01T00:00:00Z"})
    r = client.get("/api/insights/b12-trend")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_stool_trend(client):
    client.post("/api/daily-logs/", json={"date": "2026-05-01", "stool_consistency": 3})
    client.post("/api/daily-logs/", json={"date": "2026-05-02", "stool_consistency": 2})
    r = client.get("/api/insights/stool-trend")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_weekly_summary(client):
    # Create logs for a specific week (2026-03-02 is a Monday)
    client.post("/api/daily-logs/", json={
        "date": "2026-08-03",
        "energy_level": 4,
        "stool_consistency": 2,
        "pain_score": 3,
        "vomiting": True,
    })
    client.post("/api/daily-logs/", json={
        "date": "2026-08-04",
        "energy_level": 3,
        "stool_consistency": 3,
        "pain_score": 5,
    })
    r = client.get("/api/insights/weekly-summary?date=2026-08-03")
    assert r.status_code == 200
    data = r.json()
    assert data["days_logged"] >= 2
    assert data["avg_energy_level"] is not None


def test_monthly_summary(client):
    client.post("/api/daily-logs/", json={"date": "2026-09-01", "energy_level": 4})
    client.post("/api/health-markers/", json={"weight_kg": 28.0, "timestamp": "2026-09-01T00:00:00Z"})
    client.post("/api/health-markers/", json={"weight_kg": 29.0, "timestamp": "2026-09-30T00:00:00Z"})
    r = client.get("/api/insights/monthly-summary?year=2026&month=9")
    assert r.status_code == 200
    data = r.json()
    assert data["days_logged"] >= 1


def test_compliance_with_skips(client):
    # Create protocol with entries
    r = client.post("/api/treatment-protocols/", json={
        "category": "b12",
        "name": "Compliance Test",
        "schedule": {"type": "simple"},
        "start_date": "2026-01-01",
    })
    pid = r.json()["id"]

    # Administered entry
    client.post(f"/api/treatment-protocols/{pid}/entries", json={
        "scheduled_date": "2026-01-07",
        "administered_at": "2026-01-07T10:00:00Z",
    })
    # Skipped entry (past date, no administered_at)
    client.post(f"/api/treatment-protocols/{pid}/entries", json={
        "scheduled_date": "2020-01-14",
    })
    # Pending entry (future date, no administered_at)
    client.post(f"/api/treatment-protocols/{pid}/entries", json={
        "scheduled_date": "2030-01-21",
    })

    r = client.get(f"/api/insights/treatment-compliance?protocol_id={pid}")
    assert r.status_code == 200
    data = r.json()
    assert data["total_entries"] == 3
    assert data["administered"] == 1
    assert data["skipped"] == 1
    assert data["pending"] == 1
    assert data["compliance_rate"] == 0.5


def test_compliance_protocol_not_found(client):
    r = client.get("/api/insights/treatment-compliance?protocol_id=99999")
    assert r.status_code == 404
