"""API 테스트 — TestClient 로 HTTP 경로 전체(라우터→서비스→메모리저장소)를 검증."""

from fastapi.testclient import TestClient


def test_place_order_returns_201(client: TestClient) -> None:
    resp = client.post("/orders", json={"customer": "bob", "amount": 50})

    assert resp.status_code == 201
    body = resp.json()
    assert body["customer"] == "bob"
    assert body["is_large"] is False


def test_list_orders(client: TestClient) -> None:
    client.post("/orders", json={"customer": "bob", "amount": 50})

    resp = client.get("/orders")

    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_missing_order_returns_404(client: TestClient) -> None:
    resp = client.get("/orders/00000000-0000-0000-0000-000000000000")

    assert resp.status_code == 404
