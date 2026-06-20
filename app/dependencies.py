"""★ 컴포지션 루트 ★ — 구체 구현(Concrete)을 '조립'하는 유일한 장소.

여기가 헥사고날의 배선반이다: 어떤 포트에 어떤 어댑터를 꽂을지 정한다.
지금은 OrderRepository 포트에 InMemoryOrderRepository 를 꽂는다.
DB로 바꾸려면 get_repository 의 return 한 줄만 SqlAlchemyOrderRepository(...) 로 바꾸면 된다.

FastAPI 의 Annotated + Depends 가 곧 의존성 주입이다 — 별도 DI 프레임워크가 필요 없다.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.adapters.outbound.memory import InMemoryOrderRepository
from app.application.ports import OrderRepository
from app.application.services import OrderService


@lru_cache
def get_repository() -> OrderRepository:
    """저장소 구현을 고르는 단 한 곳. (테스트에선 이걸 override 해서 갈아끼운다)"""
    return InMemoryOrderRepository()


def get_order_service(
    repo: Annotated[OrderRepository, Depends(get_repository)],
) -> OrderService:
    return OrderService(repo)


# 라우터에서 `service: OrderServiceDep` 로 받으면 위 배선이 자동 주입된다.
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
