import requests


def test_task_history(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.get(f"{base_url}/history/tasks/{user_id}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    tasks = resp.json()
    assert len(tasks) >= 1, "Expected at least one ML task in history"

    statuses = {t["status"] for t in tasks}
    assert statuses & {"done", "failed", "pending", "running"}, (
        f"Unexpected task statuses: {statuses}"
    )


def test_transaction_history(base_url: str, registered_user: dict) -> None:
    user_id = registered_user["user_id"]

    resp = requests.get(f"{base_url}/history/transactions/{user_id}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    transactions = resp.json()
    assert len(transactions) >= 2, (
        f"Expected at least 2 transactions (deposit + debit), got {len(transactions)}"
    )

    types = {t["type"] for t in transactions}
    assert "credit" in types, "Expected at least one credit (deposit) transaction"
    assert "debit" in types, "Expected at least one debit (ML charge) transaction"
