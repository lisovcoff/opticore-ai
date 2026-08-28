import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """
    Test root or health endpoint to ensure the application starts up correctly.
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_resource_validation():
    """
    Test resource creation validation with invalid payload.
    """
    response = client.post("/api/v1/resources/", json={
        "name": "", 
        "cpu_capacity": -5
    })
    assert response.status_code in [400, 422]