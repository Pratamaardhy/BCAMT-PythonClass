from fastapi.testclient import TestClient

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"


def test_register_endpoint_success(client: TestClient):
    resp = client.post(
        REGISTER_URL,
        json={"email": "x@example.com", "password": "supersecret"},
    )

    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "x@example.com"
    assert "hashed_password" not in body


def test_register_duplicate_returns_409(client: TestClient):
    payload = {"email": "dup@example.com", "password": "supersecret"}

    assert client.post(REGISTER_URL, json=payload).status_code == 201
    resp = client.post(REGISTER_URL, json=payload)

    assert resp.status_code == 409


def test_register_short_password_returns_422(client: TestClient):
    resp = client.post(
        REGISTER_URL, json={"email": "x@example.com", "password": "short"}
    )

    assert resp.status_code == 422


def test_login_returns_token(client: TestClient):
    client.post(
        REGISTER_URL,
        json={"email": "y@example.com", "password": "supersecret"},
    )
    resp = client.post(
        LOGIN_URL, json={"email": "y@example.com", "password": "supersecret"}
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_returns_401(client: TestClient):
    client.post(
        REGISTER_URL,
        json={"email": "z@example.com", "password": "supersecret"},
    )
    resp = client.post(
        LOGIN_URL, json={"email": "z@example.com", "password": "badpass"}
    )

    assert resp.status_code == 401


def test_bank_accounts_require_auth(client: TestClient):
    resp = client.get("/api/v1/bank-accounts")

    assert resp.status_code == 401
