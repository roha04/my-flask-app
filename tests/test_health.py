def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "ok"
    assert "version" in data


def test_version_endpoint(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "0.1.0"
