"""도메인 예외 — 비즈니스 의미를 가진 오류. HTTP 상태코드 같은 건 여기서 모른다."""

from uuid import UUID


class OrderNotFound(Exception):
    """주어진 id의 주문이 없을 때."""

    def __init__(self, order_id: UUID) -> None:
        super().__init__(f"Order not found: {order_id}")
        self.order_id = order_id
