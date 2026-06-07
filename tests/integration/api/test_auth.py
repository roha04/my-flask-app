from tests.helpers import auth_client, login_user, register_user


def test_register_and_login(client):
    response = register_user(client)
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"

    response = login_user(client)
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


def test_me_requires_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_after_login(client):
    auth_client(client)
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_logout(client):
    auth_client(client)
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 204
    assert client.get("/api/v1/auth/me").status_code == 401


def test_duplicate_register(client):
    register_user(client)
    response = register_user(client)
    assert response.status_code == 409
