"""앱 진입점 — FastAPI 인스턴스를 만들고 라우터를 끼운다.

실행: uv run fastapi dev app/main.py   (→ http://127.0.0.1:8000/docs)
create_app() 팩토리 형태라 테스트에서 깨끗한 앱 인스턴스를 새로 만들 수 있다.
"""

from fastapi import FastAPI

from app.adapters.inbound.api.routers import router as orders_router
from app.infrastructure.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)
    app.include_router(orders_router)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
