import time
import requests
import pytest
from decimal import Decimal

_task_id: str | None = None


def _poll_task(
    base_url: str, user_id: str, task_id: str, timeout: int = 60, interval: int = 3
) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(f"{base_url}/history/tasks/{user_id}")
        assert resp.status_code == 200
        tasks = resp.json()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task and task["status"] in ("done", "failed"):
            return task
        time.sleep(interval)
    pytest.fail(f"Task {task_id} did not reach DONE/FAILED within {timeout}s")


def test_predict_insufficient_balance(base_url: str, registered_user: dict) -> None:
    resp2 = requests.post(
        f"{base_url}/auth/register",
        json={
            "email": "broke_user@example.com",
            "password": "password",
            "role": "patient",
        },
    )
    if resp2.status_code == 200:
        broke_user_id = resp2.json()["id"]
    else:
        login = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": "broke_user@example.com",
                "password": "password",
            },
        )
        assert login.status_code == 200
        broke_user_id = login.json()["user_id"]

    resp3 = requests.post(
        f"{base_url}/predict/request",
        json={
            "user_id": broke_user_id,
            "input_data": {"data": [1, 2, 3]},
            "model": "ResNet50",
        },
    )
    assert resp3.status_code == 402, (
        f"Expected 402 for insufficient balance, got {resp3.status_code}: {resp3.text}"
    )


def test_deposit_for_predict(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]
    resp = requests.post(
        f"{base_url}/balance/deposit",
        json={
            "user_id": user_id,
            "amount": "50.00",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert Decimal(str(data["balance"])) >= Decimal("1.00"), (
        f"Balance too low after deposit: {data['balance']}"
    )


def test_predict_success(base_url: str, registered_user: dict) -> None:
    global _task_id
    user_id = registered_user["user_id"]

    resp = requests.post(
        f"{base_url}/predict/request",
        json={
            "user_id": user_id,
            "input_data": {"data": [1.0, 2.0, 3.0]},
            "model": "ResNet50",
        },
    )
    assert resp.status_code == 200, (
        f"Expected 200 for predict request, got {resp.status_code}: {resp.text}"
    )
    data = resp.json()
    assert "task_id" in data
    assert data["status"] == "pending"
    _task_id = data["task_id"]


def test_predict_result_polling(base_url: str, registered_user: dict) -> None:
    assert _task_id is not None, "test_predict_success must run first"
    user_id = registered_user["user_id"]

    task = _poll_task(base_url, user_id, _task_id, timeout=60, interval=3)
    assert task["status"] == "done", (
        f"Expected task status 'done', got '{task['status']}'"
    )


def test_predict_balance_deducted(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.get(f"{base_url}/balance/{user_id}")
    assert resp.status_code == 200
    balance = Decimal(str(resp.json()["balance"]))
    assert balance < Decimal("150.00"), (
        f"Balance should have decreased after ML request, got {balance}"
    )


def test_predict_unknown_model(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.post(
        f"{base_url}/predict/request",
        json={
            "user_id": user_id,
            "input_data": {"data": [1.0]},
            "model": "NonExistentModel",
        },
    )
    assert resp.status_code == 404, (
        f"Expected 404 for unknown model, got {resp.status_code}: {resp.text}"
    )
