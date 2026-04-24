import os
import uuid
import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def registered_user(base_url: str) -> dict:
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "testpassword123"

    resp = requests.post(
        f"{base_url}/auth/register",
        json={
            "email": email,
            "password": password,
            "role": "patient",
        },
    )
    assert resp.status_code == 200, f"Registration failed: {resp.text}"
    data = resp.json()

    return {
        "user_id": data["id"],
        "email": email,
        "password": password,
    }


@pytest.fixture(scope="session")
def auth_cookie(base_url: str, registered_user: dict) -> str:
    resp = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    cookie = resp.cookies.get("access_token")
    assert cookie is not None, "No access_token cookie in login response"
    return cookie
