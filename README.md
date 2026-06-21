# _template — Team-Seuk 공통 프로젝트 템플릿

이 _template 레포지토리는 프로젝트를 시작할 때 사용할 '틀'입니다.

FastAPI 기반 **헥사고날** 파이썬 프로젝트의 골격이며, 새로운 해커톤 프로젝트를 시작할 때마다 이 레포지토리를 틀(템플릿)로 사용합니다.
GitHub **"Use this template"** 로 새 레포를 찍어 쓰면, 5명 모두 *항상 같은 구조*로 시작할 수 있게 됩니다.

> 폴더 구조가 처음이면 **먼저 [TUTORIAL.md](TUTORIAL.md) 를 읽어주세요.** — 전체적인 흐름이 나와있습니다.

---

## 1. 부트스트랩 (클론 직후 딱 1회)

```powershell
uv sync                          # 의존성 설치(.venv 자동 생성, 모두 동일 버전)
uv run pytest                    # 환경 확인 — 다 통과하면 준비 끝
```

> uv 가 없으면(머신당 1회): `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` 후 **새 터미널**을 연다.

## 2. 실행

```powershell
uv run fastapi dev app/main.py      # -> http://127.0.0.1:8000/docs (대화형 API 문서)
```

## 3. THE ONE RULE — import 는 안쪽으로만 향한다

- `adapters/` · `main.py` · `dependencies.py`  →  `application/` · `domain/` 호출 가능
- `application/`  →  `domain/` 만
- `domain/`  →  아무것도(파이썬 표준 라이브러리만)

판별법: `fastapi` 를 쓰면 **inbound 어댑터**, `sqlalchemy/httpx` 를 쓰면 **outbound 어댑터**, 둘 다 아니면 **domain/application**.
이 규칙은 CI 가 `uv run lint-imports` 로 **자동 강제**한다.

## 4. 폴더 한눈에

```text
app/
├── main.py            앱 진입점(FastAPI 생성)
├── dependencies.py    ★조립소★ 어떤 구현을 꽂을지 정하는 유일한 곳
├── domain/            순수 비즈니스(엔티티·규칙). 프레임워크 import 금지
├── application/       유스케이스(services) + 계약(ports)
├── adapters/
│   ├── inbound/api/   HTTP 입구(라우터·요청응답 스키마)
│   └── outbound/      저장소 구현(memory / 나중에 sql)
└── infrastructure/    설정 등 얇은 기술 계층
tests/                 app 미러링(unit / api)
```

## 5. "이런 거 추가하려면 어디?" (빠른 표)

| 추가할 것 | 어디 | 
|---|---|
| 새 비즈니스 규칙/계산 | `domain/models.py` 또는 `application/services.py` |
| 새 HTTP 엔드포인트 | `adapters/inbound/api/routers.py` (+ `schemas.py`) |
| 새 저장소/외부 API 호출 | `adapters/outbound/` 에 포트를 만족하는 클래스 |
| 구현 교체(메모리→DB) | `dependencies.py` 의 `get_repository` 한 줄 |
| 설정값 | `infrastructure/settings.py` |

## 6. 명령어

| 목적 | 명령 |
|---|---|
| 실행 | `uv run fastapi dev app/main.py` |
| 테스트 | `uv run pytest` |
| 린트/포맷 | `uv run ruff check .` / `uv run ruff format .` |
| 타입체크 | `uv run mypy` |
| 경계 검사 | `uv run lint-imports` |
| 의존성 추가 | `uv add <패키지>`  → `uv.lock` 자동 갱신 → **커밋** |

> ⚠️ `pip install` · `python -m venv` 금지. 잠금(uv.lock)을 우회해 팀원 환경이 갈라진다. 항상 `uv add/sync/run`.

협업 흐름(브랜치·PR)은 [TUTORIAL.md](TUTORIAL.md) 7장 참고.
