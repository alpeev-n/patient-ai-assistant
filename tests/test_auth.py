import requests


def test_register_success(base_url: str, registered_user: dict) -> None:
    assert registered_user["user_id"] is not None
    assert "@" in registered_user["email"]


def test_register_duplicate(base_url: str, registered_user: dict) -> None:
    resp = requests.post(
        f"{base_url}/auth/register",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
            "role": "patient",
        },
    )
    assert resp.status_code in (400, 409), (
        f"Expected 400 or 409 for duplicate email, got {resp.status_code}: {resp.text}"
    )


def test_login_success(base_url: str, registered_user: dict, auth_cookie: str) -> None:
    assert auth_cookie is not None
    assert len(auth_cookie) > 0


def test_login_wrong_password(base_url: str, registered_user: dict) -> None:
    resp = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": registered_user["email"],
            "password": "wrongpassword",
        },
    )
    assert resp.status_code == 401, (
        f"Expected 401 for wrong password, got {resp.status_code}: {resp.text}"
    )


def test_login_unknown_email(base_url: str) -> None:
    resp = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "anypassword",
        },
    )
    assert resp.status_code == 401, (
        f"Expected 401 for unknown email, got {resp.status_code}: {resp.text}"
    )
