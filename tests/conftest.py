"""pytest 공용 픽스처.

핵심: 테스트할 땐 컴포지션 루트의 get_repository 를 override 해서
메모리 저장소를 끼워 넣는다 → DB/네트워크 없이 앱 전체를 검증할 수 있다.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.adapters.outbound.memory import InMemoryOrderRepository
from app.application.ports import OrderRepository
from app.application.services import OrderService
from app.dependencies import get_repository
from app.main import create_app


@pytest.fixture
def repo() -> OrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def service(repo: OrderRepository) -> OrderService:
    return OrderService(repo)


@pytest.fixture
def client(repo: OrderRepository) -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_repository] = lambda: repo
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
