def register_and_login(client, email):
    client.post(
        "/api/v1/auth/register", json={"email": email, "password": "supersecret"}
    )
    res = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "supersecret"}
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_bank_account(client, headers, account_number):
    return client.post(
        "/api/v1/bank-accounts",
        headers=headers,
        json={
            "account_number": account_number,
            "account_name": "Name",
            "bank_name": "Bank ABC",
            "balance": "1000",
        },
    )


def create_user_account(client, headers, bank_account_id, label=None, is_primary=False):
    return client.post(
        "/api/v1/user-accounts",
        headers=headers,
        json={
            "bank_account_id": bank_account_id,
            "label": label,
            "is_primary": is_primary,
        },
    )


def update_user_account(client, headers, user_account_id, **payload):
    return client.put(
        f"/api/v1/user-accounts/{user_account_id}", headers=headers, json=payload
    )


def delete_user_account(client, headers, user_account_id):
    return client.delete(f"/api/v1/user-accounts/{user_account_id}", headers=headers)


# TEST


def test_create_success(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    bank_account_id = bank_resp.json()["id"]

    response = create_user_account(client, headers, bank_account_id, label="Gaji")

    assert response.status_code == 201
    body = response.json()
    assert body["bank_account_id"] == bank_account_id
    assert body["status"] == "active"


def test_create_tanpa_token(client):
    response = create_user_account(client, {}, 1)

    assert response.status_code == 401


def test_create_bank_account_milik_user_lain(client):
    headers1 = register_and_login(client, "test1@example.com")
    headers2 = register_and_login(client, "test2@example.com")
    bank_resp = create_bank_account(client, headers1, "1234567890")
    bank_account_id = bank_resp.json()["id"]

    response = create_user_account(client, headers2, bank_account_id)

    assert response.status_code == 404


def test_create_duplikat(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    bank_account_id = bank_resp.json()["id"]

    resp1 = create_user_account(client, headers, bank_account_id)
    assert resp1.status_code == 201

    resp2 = create_user_account(client, headers, bank_account_id)
    assert resp2.status_code == 409


def test_list_hanya_milik_user(client):
    headers1 = register_and_login(client, "test1@example.com")
    headers2 = register_and_login(client, "test2@example.com")
    bank_resp1 = create_bank_account(client, headers1, "1111111111")
    bank_resp2 = create_bank_account(client, headers2, "2222222222")
    create_user_account(client, headers1, bank_resp1.json()["id"])
    create_user_account(client, headers2, bank_resp2.json()["id"])

    response = client.get("/api/v1/user-accounts", headers=headers1)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["bank_account_id"] == bank_resp1.json()["id"]


def test_get_by_id_success(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    created = create_user_account(client, headers, bank_resp.json()["id"])
    user_account_id = created.json()["id"]

    response = client.get(f"/api/v1/user-accounts/{user_account_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user_account_id


def test_get_by_id_milik_user_lain(client):
    headers1 = register_and_login(client, "test1@example.com")
    headers2 = register_and_login(client, "test2@example.com")
    bank_resp = create_bank_account(client, headers1, "1234567890")
    created = create_user_account(client, headers1, bank_resp.json()["id"])
    user_account_id = created.json()["id"]

    response = client.get(f"/api/v1/user-accounts/{user_account_id}", headers=headers2)

    assert response.status_code == 404


def test_update_label_success(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    created = create_user_account(client, headers, bank_resp.json()["id"], label="Lama")
    user_account_id = created.json()["id"]

    response = update_user_account(client, headers, user_account_id, label="Baru")

    assert response.status_code == 200
    assert response.json()["label"] == "Baru"


def test_update_status_invalid(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    created = create_user_account(client, headers, bank_resp.json()["id"])
    user_account_id = created.json()["id"]

    response = update_user_account(client, headers, user_account_id, status="bogus")

    assert response.status_code == 422


def test_delete_success(client):
    headers = register_and_login(client, "test@example.com")
    bank_resp = create_bank_account(client, headers, "1234567890")
    created = create_user_account(client, headers, bank_resp.json()["id"])
    user_account_id = created.json()["id"]

    response = delete_user_account(client, headers, user_account_id)

    assert response.status_code == 204


def test_delete_milik_user_lain(client):
    headers1 = register_and_login(client, "test1@example.com")
    headers2 = register_and_login(client, "test2@example.com")
    bank_resp = create_bank_account(client, headers1, "1234567890")
    created = create_user_account(client, headers1, bank_resp.json()["id"])
    user_account_id = created.json()["id"]

    response = delete_user_account(client, headers2, user_account_id)

    assert response.status_code == 404
