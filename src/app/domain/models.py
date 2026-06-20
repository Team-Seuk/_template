"""도메인 엔티티 — 가장 안쪽 고리. 순수 파이썬, 표준 라이브러리만 쓴다.

여기에는 fastapi / sqlalchemy / pydantic 같은 프레임워크를 절대 import 하지 않는다.
비즈니스 데이터와 그 데이터에 붙는 규칙(메서드)이 함께 산다.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Order:
    """주문 한 건. 프레임워크와 무관한 순수 도메인 객체."""

    customer: str
    amount: int
    id: UUID = field(default_factory=uuid4)

    def is_large(self) -> bool:
        """도메인 규칙의 예시 — '큰 주문'의 정의가 데이터 옆에 산다."""
        return self.amount >= 100
