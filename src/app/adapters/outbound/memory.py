"""outbound(driven) 어댑터 — 앱이 '포트를 통해 호출'하는 바깥쪽 구현(메모리 저장소).

OrderRepository 포트를 상속 없이 '구조적으로' 만족한다(메서드 시그니처만 맞으면 됨).
첫날부터 이걸로 동작하므로, DB가 없어도 5명이 병렬로 기능을 만들고 테스트할 수 있다.
DB가 필요해지면 같은 포트를 만족하는 sql.py 를 만들어 dependencies.py 에서 한 줄만 바꾼다.
(DB 추가법은 TUTORIAL.md 참고)
"""

from uuid import UUID

from app.domain.errors import OrderNotFound
from app.domain.models import Order


class InMemoryOrderRepository:
    """프로세스 메모리(dict)에 주문을 저장하는 저장소."""

    def __init__(self) -> None:
        self._orders: dict[UUID, Order] = {}

    def add(self, order: Order) -> None:
        self._orders[order.id] = order

    def get(self, order_id: UUID) -> Order:
        try:
            return self._orders[order_id]
        except KeyError:
            raise OrderNotFound(order_id) from None

    def list_all(self) -> list[Order]:
        return list(self._orders.values())
