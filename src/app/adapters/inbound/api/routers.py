"""inbound(driving) 어댑터 — 바깥에서 앱을 '호출'하는 입구(HTTP).

여기서만 fastapi 를 import 한다(=inbound 어댑터의 표식).
하는 일: HTTP 요청을 받아 → 서비스(유스케이스)를 호출 → 결과를 응답 스키마로 변환.
비즈니스 로직은 절대 여기 두지 않는다(그건 application/domain 의 몫).
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.adapters.inbound.api.schemas import OrderResponse, PlaceOrderRequest
from app.dependencies import OrderServiceDep
from app.domain.errors import OrderNotFound
from app.domain.models import Order

router = APIRouter(prefix="/orders", tags=["orders"])


def _to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        customer=order.customer,
        amount=order.amount,
        is_large=order.is_large(),
    )


@router.post("", response_model=OrderResponse, status_code=201)
def place_order(body: PlaceOrderRequest, service: OrderServiceDep) -> OrderResponse:
    order = service.place_order(customer=body.customer, amount=body.amount)
    return _to_response(order)


@router.get("", response_model=list[OrderResponse])
def list_orders(service: OrderServiceDep) -> list[OrderResponse]:
    return [_to_response(o) for o in service.list_orders()]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, service: OrderServiceDep) -> OrderResponse:
    try:
        return _to_response(service.get_order(order_id))
    except OrderNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
