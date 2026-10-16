import os
import pytest
from unittest.mock import patch, MagicMock
from app import app, User
import database

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testkey"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client

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

def test_get_connection_fallback():
    with patch.dict(os.environ, {}, clear=True):
        with patch("database.psycopg.connect") as mock_connect:
            database.get_connection()
            mock_connect.assert_called_once_with("postgresql://postgres:password@localhost:5432/employee_db")

def test_get_connection_url():
    test_url = "postgresql://user:pass@remote:5432/mydb"
    with patch.dict(os.environ, {"DATABASE_URL": test_url}):
        with patch("database.psycopg.connect") as mock_connect:
            database.get_connection()
            mock_connect.assert_called_once_with(test_url)

@patch("app.get_user_by_username")
@patch("app.register_user")
def test_register_post(mock_register, mock_get_user, client):
    mock_get_user.return_value = None
    response = client.post("/register", data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"
    mock_register.assert_called_once_with("newuser", "new@example.com", "password123")

@patch("app.get_user_by_username")
def test_login_invalid_user(mock_get_user, client):
    mock_get_user.return_value = None
    response = client.post("/login", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

@patch("app.get_employees")
def test_dashboard_authenticated(mock_get_employees, client):
    mock_get_employees.return_value = [(1, "Alice", "alice@example.com", "Eng", "Dev", 100000, 1)]
    with client.session_transaction() as sess:
        sess["_user_id"] = "1"
    with patch("app.get_user_by_id") as mock_get_user_by_id:
        mock_get_user_by_id.return_value = (1, "alice", "alice@example.com")
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert b"Alice" in response.data
