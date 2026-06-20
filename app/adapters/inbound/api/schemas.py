"""inbound 어댑터의 입출력 모델(Pydantic). HTTP 가장자리에서만 쓴다.

⚠️ 이 스키마는 '도메인 객체'가 아니다. 도메인(Order)과 분리해서 두는 이유:
   HTTP 표현이 바뀌어도 도메인이 흔들리지 않게 하려는 것. 둘을 합치면 계층이 다시 엉킨다.
"""

from uuid import UUID

from pydantic import BaseModel


class PlaceOrderRequest(BaseModel):
    customer: str
    amount: int


class OrderResponse(BaseModel):
    id: UUID
    customer: str
    amount: int
    is_large: bool
