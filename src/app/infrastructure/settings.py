"""앱 설정 — .env 파일이나 환경변수에서 값을 읽는다(기술 계층, 비즈니스 로직 아님).

⚠️ 모든 필드에 '기본값'을 준다. 그래야 .env 없이 갓 클론한 상태에서도 앱이 그냥 뜬다.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "app"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """설정을 한 번만 읽어 캐시한다."""
    return Settings()
