def register_user(client, email="user@example.com", password="secret123", name="Test User"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "name": name},
    )


def login_user(client, email="user@example.com", password="secret123"):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


def auth_client(client):
    response = register_user(client)
    assert response.status_code == 201
    response = login_user(client)
    assert response.status_code == 200
    return client
