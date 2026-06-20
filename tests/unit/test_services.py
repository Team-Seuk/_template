"""유닛 테스트 — 서비스(유스케이스)를 메모리 저장소로 직접 검증. 빠르고 DB가 필요 없다."""

from uuid import uuid4

import pytest

from app.application.services import OrderService
from app.domain.errors import OrderNotFound


def test_place_and_get_order(service: OrderService) -> None:
    order = service.place_order(customer="alice", amount=120)

    fetched = service.get_order(order.id)

    assert fetched is order
    assert order.is_large() is True


def test_get_missing_order_raises(service: OrderService) -> None:
    with pytest.raises(OrderNotFound):
        service.get_order(uuid4())
