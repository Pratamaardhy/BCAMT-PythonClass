
def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "securepassword"}, )
    
    assert response.status_code == 201
    
    assert response.json().get("hashed_password") != "securepassword"

    
def test_register_duplicate_email(client):
    Response = client.post(
        "/api/v1/auth/register",
        json={"email": "dupp@gmail.com", "password": "securepassword"}, )
    
    assert Response.status_code == 201
    
    assert Response.json().get("hashed_password") != "securepassword"
    
    Response = client.post(
            "/api/v1/auth/register",
            json={"email": "dupp@gmail.com", "password": "password123"},)
    
    assert Response.status_code == 409 
    
def test_password_pendek(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "pendekbanget@gmail.com", "password": "123456"}, )
    
    assert response.status_code == 422
    
def test_login_berhasil(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@gmail.com", "password": "securepassword"}, )
    
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@gmail.com", "password": "securepassword"}, )
    
    assert response.status_code == 200
    
def test_login_salah(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@gmail.com", "password": "securepassword"}, )
    
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@gmail.com", "password": "wrongpassword"}, )
    
    assert response.status_code == 401