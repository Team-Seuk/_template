"""유스케이스(서비스) — 애플리케이션의 '할 일'을 조율한다.

domain 과 포트(ports)만 의존한다. 구체적인 DB/HTTP 는 전혀 모른다.
그래서 테스트할 때 메모리 저장소를 끼워 넣으면 DB 없이도 전부 검증된다.
"""

from uuid import UUID

from app.application.ports import OrderRepository
from app.domain.models import Order


class OrderService:
    """주문 관련 유스케이스 묶음. 저장소는 '포트'로 주입받는다(생성자 주입)."""

    def __init__(self, repo: OrderRepository) -> None:
        self._repo = repo

    def place_order(self, customer: str, amount: int) -> Order:
        order = Order(customer=customer, amount=amount)
        self._repo.add(order)
        return order

    def get_order(self, order_id: UUID) -> Order:
        return self._repo.get(order_id)

    def list_orders(self) -> list[Order]:
        return self._repo.list_all()
