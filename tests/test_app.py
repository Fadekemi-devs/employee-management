import os
import tempfile
import pytest
from unittest.mock import patch
from app import app
import database

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testkey"
    app.config["WTF_CSRF_ENABLED"] = False

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    with patch.dict(os.environ, {"SQLITE_DB_PATH": db_path, "DATABASE_URL": ""}, clear=True):
        database.create_table()
        with app.test_client() as client:
            yield client

    if os.path.exists(db_path):
        os.remove(db_path)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Employee Management System" in response.data

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200

def test_sqlite_fallback_and_crud(client):
    reg_resp = client.post("/register", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert reg_resp.status_code == 200

    login_resp = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    assert login_resp.status_code == 200
    assert b"Employee Directory" in login_resp.data

def test_login_invalid_password(client):
    client.post("/register", data={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "password123"
    })
    response = client.post("/login", data={
        "username": "testuser2",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
