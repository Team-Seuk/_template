"""포트 = 계약(인터페이스). 애플리케이션이 '바깥 세계'에 요구하는 능력의 명세.

이 템플릿은 포트를 딱 하나만 둔다: OrderRepository(저장소).
typing.Protocol 을 쓰므로, 이 메서드들을 가진 클래스는 상속 없이도 자동으로 '포트를 만족'한다.

⚠️ 규칙: 진짜로 구현을 갈아끼우는 것만 포트로 만든다(예: 메모리 저장소 ↔ DB 저장소).
   "혹시 몰라서" 모든 의존성을 포트로 감싸지 말 것 — 해커톤에선 그게 발목을 잡는다.
"""

from typing import Protocol
from uuid import UUID

from app.domain.models import Order


class OrderRepository(Protocol):
    """주문을 저장/조회하는 능력. 구현체(메모리/DB)는 adapters/outbound 에 둔다."""

    def add(self, order: Order) -> None: ...

    def get(self, order_id: UUID) -> Order: ...

    def list_all(self) -> list[Order]: ...
