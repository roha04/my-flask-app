def test_login_page(client):
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 200
    assert "Login" in response.text


def test_dashboard_redirects_to_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_dashboard_after_auth(client):
    from tests.helpers import auth_client

    auth_client(client)
    response = client.get("/")
    assert response.status_code == 200
    assert "Dashboard" in response.text
    assert "Active applications" in response.text


def test_applications_kanban_page(client):
    from tests.helpers import auth_client

    auth_client(client)
    response = client.get("/applications")
    assert response.status_code == 200
    assert "Applications" in response.text
