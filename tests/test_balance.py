import requests
from decimal import Decimal


def test_get_initial_balance(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]
    resp = requests.get(f"{base_url}/balance/{user_id}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert Decimal(str(data["balance"])) == Decimal("0.00"), (
        f"Expected initial balance 0, got {data['balance']}"
    )


def test_deposit(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.post(
        f"{base_url}/balance/deposit",
        json={
            "user_id": user_id,
            "amount": "100.00",
        },
    )
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert Decimal(str(data["balance"])) == Decimal("100.00"), (
        f"Expected balance 100.00 after deposit, got {data['balance']}"
    )


def test_deposit_negative(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.post(
        f"{base_url}/balance/deposit",
        json={
            "user_id": user_id,
            "amount": "-50.00",
        },
    )
    assert resp.status_code == 422, (
        f"Expected 422 for negative deposit, got {resp.status_code}: {resp.text}"
    )
