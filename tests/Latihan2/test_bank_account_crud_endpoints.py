def register_and_login(client, email):
    client.post(
        "/api/v1/auth/register", json={"email": email, "password": "supersecret"}
    )
    res = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "supersecret"}
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_account(client, headers, account_number, balance="0"):
    return client.post(
        "/api/v1/bank-accounts",
        headers=headers,
        json={
            "account_number": account_number,
            "account_name": "Name",
            "bank_name": "Bank ABC",
            "balance": balance,
        },
    )

def update_account(client, headers, account_id, account_name, bank_name, balance):
    return client.put(
        f"/api/v1/bank-accounts/{account_id}",
        headers=headers,
        json={
            "account_name": account_name,
            "bank_name": bank_name,
            "balance": balance,
        },
    )
    
def delete_account(client, header, account_id):
    return client.delete(
        f"/api/v1/bank-accounts/{account_id}",
        headers = header
    )
    

#TEST

def test_create_account_success(client):
    headers = register_and_login(client, "test@example.com")
    
    response = create_account(client, headers, "1234567890", balance="1000")
    
    assert response.status_code == 201
    body = response.json()
    assert body["account_number"] == "1234567890"
    assert body["balance"] == "1000.00"
    
def test_create_account_duplicate_account_number(client):
    headers = register_and_login(client, "test@example.com")
    
    resp = create_account(client, headers, "1234567890", balance="1000")
    assert resp.status_code == 201
    
    resp2 = create_account(client, headers, "1234567890", balance="500")
    assert resp2.status_code == 409

def test_create_account_tanpa_token(client):
    response = create_account(client, headers={}, account_number="1234567890", balance="1000")
    
    assert response.status_code == 401
    
def test_update_account_success(client):
    headers = register_and_login(client, "test@example.com")
    resp = create_account(client, headers, "1234567890", balance="1000")
    account_id = resp.json()["id"]
    
    update_resp = update_account(client, headers, account_id, "Updated Name", "Updated Bank", 2000)
    assert update_resp.status_code == 200
    assert update_resp.json()["account_name"] == "Updated Name"
    assert update_resp.json()["bank_name"] == "Updated Bank"
    assert update_resp.json()["balance"] == "2000.00"
    
def test_update_account_punya_user_lain(client):
    headers1 = register_and_login(client, "test1@example.com")
    headers2 = register_and_login(client, "test2@example.com")
    
    resp = create_account(client, headers1, "1234567890", balance="1000")
    account_id = resp.json()["id"]
    
    update_resp = update_account(client, headers2, account_id, "Updated Name", "Updated Bank", 2000)
    assert update_resp.status_code == 404
    
def test_update_balance_negatif(client):
    headers = register_and_login(client, "test@example.com")
    resp = create_account(client, headers, "1234567890", balance="1000")
    account_id = resp.json()["id"]

    update_resp = update_account(client, headers, account_id, "Updated Name", "Updated Bank", -500)
    assert update_resp.status_code == 422
    
def test_delete(client):
    headers = register_and_login(client, "test@gmail.com")
    resp = create_account(client, headers, "123123123", balance="5000")
    account_id = resp.json()["id"]
    
    delete_resp = delete_account(client, headers, account_id)
     
    assert delete_resp.status_code == 204
    
def test_delete_punya_orang_lain(client):
    headers1 = register_and_login(client, "test@gmail.com")
    headers2 = register_and_login(client, "test2@gmail.com")
    
    resp1 = create_account(client, headers1, "123123123", balance="5000")
    account_id1 = resp1.json()["id"]
    
    resp2 = create_account(client, headers1, "321321321", balance="5000")
    account_id2 = resp2.json()["id"]
    
    delete_resp = delete_account(client, headers2, account_id1)
    assert delete_resp.status_code==404
