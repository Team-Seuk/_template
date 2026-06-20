# TUTORIAL — 폴더 구조 설명

이 문서로 각 폴더가 뭔지, 요청이 어떻게 흐르는지, 새 기능을 어디에 넣는지를 다 알 수 있다.
예제로 "주문(Order)" 도메인이 이미 들어 있으니, 그걸 따라가며 확인해본다.

---

## 0. 한 줄 요약

> **바깥(웹·DB)과 안쪽(비즈니스 로직)을 분리하고, 그 사이를 "포트(계약)"로 잇는다.**
> 그래서 DB가 없어도 비즈니스 로직을 만들고 테스트할 수 있고, 나중에 DB를 갈아끼워도 안쪽 코드는 안 바뀐다.

이걸 '헥사고날 아키텍처'(= 포트 & 어댑터)라고 부른다. 이 템플릿은 해커톤 속도를 위해 꼭 필요한 부분만 남긴 '경량 헥사고날' 이라고 생각하면 됨.

---

## 1. 비유로 이해하기

'컴퓨터'를 예시로 든다.

핵심 로직(domain + application) => 컴퓨터 본체. 계산만 함.
진짜 가치(음식)가 여기서 만들어짐. 손님이 웹으로 주문하든 전화로 하든 주방은 신경 안 씀. 그냥 주문 들어오면 음식을 내면 됨.

포트(ports) => 본체 뒤에 뚫린 USB·HDMI 구멍. "이 규격이면 뭐든지 OK"라는 약속임.

어댑터(adapters) => 주변기기.
inbound_adapters(들어오는 쪽) => 키보드&마우스. 본체로 입력을 넣는 존재.
outbound_adapters(나가는 쪽) => 모니터·프린터. 본체에서 출력을 빼는 존재.

핵심: 규격(포트)만 맞으면 뭘 가져와도 쓸 수 있다. 그것이 핵사고날의 최고 장점.

---

## 2. THE ONE RULE (이거 하나만 지키면 된다)

> **import 는 항상 안쪽으로만 향한다.**

```
 바깥 ────────────────────────────▶ 안쪽
 adapters/        application/        domain/
 main.py          (services, ports)   (models, errors)
 dependencies.py

 ✅ 바깥이 안쪽을 import 한다        (adapters → application → domain)
 ❌ 안쪽이 바깥을 import 한다        (domain 이 fastapi 를 import? 절대 금지)
```

외우기 쉬운 판별법:

- 파일이 **`fastapi`** 를 import 한다 → 그건 **inbound 어댑터**다 (`adapters/inbound/`).
- 파일이 **`sqlalchemy` / `httpx`**(DB·외부 API) 를 import 한다 → **outbound 어댑터**다 (`adapters/outbound/`).
- **둘 다 아니다** → 그건 **domain/ 또는 application/** 에 속한다.

이 규칙은 사람이 깜빡해도 **CI가 자동으로 잡는다** (`uv run lint-imports`). 어기면 PR이 빨갛게 뜬다.

---

## 3. 폴더·파일 전수 설명

```text
_template/
├── pyproject.toml          # 프로젝트 설정 한 곳: 의존성 + ruff/mypy/pytest/import-linter 설정 전부
├── uv.lock                 # 패키지 정확한 버전 잠금. ★커밋★ → 5명이 똑같은 환경
├── .python-version         # 파이썬 버전 고정(3.12). uv 가 알아서 받아온다
├── .env.example            # 설정 견본 → 복사해서 .env 만들기
├── .gitignore / .gitattributes
├── .pre-commit-config.yaml # 커밋 직전 자동 포맷·검사
├── README.md               # 빠른 시작 + 명령어
├── CONTRIBUTING.md         # 브랜치·PR 규칙
├── TUTORIAL.md             # (이 문서)
├── .github/                # GitHub 설정(코드오너·PR양식·CI)
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   └── workflows/ci.yml    # PR마다 lint·type·import·test 자동 실행
│
├── app/                    # ← 실제 코드(패키지). 열면 바로 이 안에 구조가 보인다
│   │
│   ├── main.py             # 【진입점】 FastAPI 앱을 만들고 라우터를 끼운다
│   ├── dependencies.py     # 【조립소 = 컴포지션 루트】 어떤 구현을 꽂을지 정하는 ★유일한★ 곳
│   │
│   ├── domain/             # 【가장 안쪽】 순수 비즈니스. 프레임워크 import 절대 금지
│   │   ├── models.py       #   엔티티·값객체 (예: Order). 데이터 + 그 데이터의 규칙(메서드)
│   │   └── errors.py       #   비즈니스 예외 (예: OrderNotFound)
│   │
│   ├── application/        # 【유스케이스】 "할 일"을 조율. domain 과 ports 만 안다
│   │   ├── ports.py        #   ★포트(계약)★ — Protocol 로 "저장소는 이런 메서드를 가진다"만 선언
│   │   └── services.py     #   OrderService — place_order/get_order/list_orders 같은 실제 시나리오
│   │
│   ├── adapters/           # 【가장자리】 바깥 세상과 연결. 안쪽을 import, 안쪽은 이걸 모름
│   │   ├── inbound/api/    #   들어오는 쪽(HTTP)
│   │   │   ├── routers.py  #     FastAPI 라우터: 요청 받기 → 서비스 호출 → 응답
│   │   │   └── schemas.py  #     요청/응답 모델(Pydantic). 도메인과 분리된 "겉모습"
│   │   └── outbound/       #   나가는 쪽(저장소·외부)
│   │       └── memory.py   #     InMemoryOrderRepository — 포트를 만족하는 메모리 구현(첫날부터 동작)
│   │
│   └── infrastructure/     # 【얇은 기술 계층】 비즈니스 아님
│       └── settings.py     #   .env/환경변수 읽기(모든 값에 기본값)
│
└── tests/                  # app 을 거울처럼 따라감
    ├── conftest.py         #   공용 픽스처: 메모리 저장소를 끼워 넣는 TestClient
    ├── unit/               #   서비스/도메인 단위 테스트(빠름, DB 없음)
    └── api/                #   HTTP 경로 전체 테스트(TestClient)
```

### 각 계층을 "언제 건드리나"

- **domain/** — "이 서비스의 진짜 규칙"이 바뀔 때. (예: 큰 주문 기준이 100→200)
- **application/** — 새 시나리오/유스케이스가 생길 때. (예: "주문 취소" 기능)
- **adapters/inbound/** — 새 HTTP 엔드포인트, 요청/응답 모양이 바뀔 때.
- **adapters/outbound/** — 저장 방식·외부 연동이 바뀔 때. (메모리→DB, 결제 API 추가 등)
- **dependencies.py** — "어떤 구현을 쓸지" 바뀔 때. (메모리 repo → SQL repo 교체)
- **infrastructure/** — 설정값이 늘 때.

---

## 4. 요청 하나가 흐르는 길 (POST /orders 따라가기)

손님이 `POST /orders {"customer":"alice","amount":120}` 를 보냈다고 하자.

```
1. adapters/inbound/api/routers.py   place_order() 가 요청을 받음
   - schemas.PlaceOrderRequest 로 본문 검증(customer, amount)
2.   └▶ dependencies.py 가 OrderService 를 자동 주입(메모리 저장소가 꽂힌 상태)
3.        └▶ application/services.py   OrderService.place_order() 호출
4.             └▶ domain/models.py     Order(customer, amount) 생성 (규칙: is_large())
5.             └▶ application/ports.py  repo.add(order)  ← "포트"를 통해 저장 요청
6.                  └▶ adapters/outbound/memory.py  실제로 dict 에 저장
7. 결과 Order 를 schemas.OrderResponse 로 변환해 201 로 응답
```

눈여겨볼 점: **3~5단계(주방)는 "메모리에 저장되는지 DB에 저장되는지" 전혀 모른다.** 그냥 "포트(repo)"에 부탁할 뿐. 그래서 나중에 6단계만 SQL 구현으로 바꾸면 1~5는 그대로다.

---

## 5. 실습: 새 엔드포인트 추가해보기

"가장 큰 주문 조회" `GET /orders/largest` 를 추가한다고 하자. **THE ONE RULE 순서대로 안→밖**:

1. **application/services.py** 에 유스케이스 추가:
   ```python
   def largest_order(self) -> Order:
       orders = self._repo.list_all()
       if not orders:
           raise OrderNotFound(...)   # 또는 전용 예외
       return max(orders, key=lambda o: o.amount)
   ```
2. **adapters/inbound/api/routers.py** 에 엔드포인트 추가:
   ```python
   @router.get("/largest", response_model=OrderResponse)
   def largest_order(service: OrderServiceDep) -> OrderResponse:
       return _to_response(service.largest_order())
   ```
3. **tests/** 에 테스트 추가 → `uv run pytest`.

저장소(outbound)나 dependencies 는 **건드릴 필요 없다.** 기존 포트로 충분하니까. 이게 잘 설계된 신호다.

---

## 6. DB가 필요해지면 (포트 1개의 위력)

해커톤 중반에 진짜 DB가 필요해졌다. **안쪽 코드는 안 바꾼다.** outbound 어댑터만 하나 더 만들고, 조립소에서 한 줄 바꾼다.

1. DB 패키지 추가: `uv add sqlalchemy`
2. `adapters/outbound/sql.py` 새로 만들기 — `OrderRepository` 포트와 **같은 메서드**(add/get/list_all)를 가진 클래스:
   ```python
   class SqlAlchemyOrderRepository:
       def __init__(self, session): ...
       def add(self, order): ...
       def get(self, order_id): ...
       def list_all(self): ...
   ```
3. `dependencies.py` 의 `get_repository` **한 줄만** 교체:
   ```python
   def get_repository() -> OrderRepository:
       return SqlAlchemyOrderRepository(get_session())   # ← 메모리 → SQL
   ```

`services.py`, `routers.py`, `domain/` 는 **한 글자도 안 바뀐다.** 테스트도 그대로 메모리 저장소로 빠르게 돈다. 이게 포트를 하나 둔 이유 전부다.

> 💡 반대로, "혹시 몰라서" 모든 것에 포트를 만들지 마라. **진짜로 구현을 갈아끼우는 것(저장소)만** 포트다. 나머지는 그냥 직접 호출. 해커톤에선 추상화도 비용이다.

---

## 7. 환경·명령어 (외울 건 이거뿐)

| 하고 싶은 것            | 명령                                                                    |
| ----------------------- | ----------------------------------------------------------------------- |
| 처음 세팅               | `uv sync` → `Copy-Item .env.example .env` → `uv run pre-commit install` |
| 앱 실행                 | `uv run fastapi dev app/main.py` (→ `/docs`)                        |
| 테스트                  | `uv run pytest`                                                         |
| 포맷·린트               | `uv run ruff format .` / `uv run ruff check .`                          |
| 타입 검사               | `uv run mypy`                                                           |
| 경계(THE ONE RULE) 검사 | `uv run lint-imports`                                                   |
| 패키지 추가             | `uv add <이름>` (→ `uv.lock` 자동 갱신 → **커밋**)                      |

**왜 전부 `uv run` 으로 시작?** `uv` 가 `uv.lock` 에 잠긴 정확한 버전으로 실행해 주기 때문. 그래서 5명 결과가 항상 같다. `pip install` 이나 `python xxx.py` 를 직접 쓰면 잠금이 깨져 "내 컴퓨터에선 됐는데"가 시작된다.

---

## 8. 자주 하는 실수 & 함정

- ❌ **`domain/` 이나 `application/` 안에서 `fastapi`/`sqlalchemy` import** → THE ONE RULE 위반. CI가 막는다. 비즈니스 로직은 프레임워크를 몰라야 한다.
- ❌ **라우터(routers.py)에 비즈니스 로직 작성** → 라우터는 "받아서 서비스에 넘기고 응답"만. 계산·규칙은 services/domain.
- ❌ **도메인 객체(Order)를 그대로 API 응답으로** → 반드시 `schemas.OrderResponse` 로 변환. 안 그러면 겉모습과 도메인이 다시 엉킨다.
- ❌ **저장소를 라우터 안에서 `InMemoryOrderRepository()` 직접 생성** → 조립은 `dependencies.py` 한 곳에서만. 안 그러면 테스트에서 못 갈아끼운다.
- ❌ **`pip install` / `python -m venv`** → `uv add` / `uv sync` 만.
- ❌ **`.env` 커밋** → `.gitignore` 가 막지만, 비밀은 절대 올리지 않는다. 견본은 `.env.example`.
- ❌ **`uv.lock` 을 `.gitignore` 에 추가** → 절대. 이걸 커밋해야 환경이 같아진다.

---

## 9. 용어 사전

| 용어                                 | 뜻                                                                  |
| ------------------------------------ | ------------------------------------------------------------------- |
| **도메인(domain)**                   | 이 서비스의 진짜 알맹이(데이터 + 비즈니스 규칙). 프레임워크와 무관. |
| **유스케이스(application/services)** | "주문을 넣는다" 같은 시나리오. 도메인과 포트를 조율.                |
| **포트(port)**                       | 안쪽이 바깥에 거는 계약(인터페이스). 여기선 `OrderRepository`.      |
| **어댑터(adapter)**                  | 포트를 실제 세상에 연결하는 구현. inbound(들어옴)·outbound(나감).   |
| **inbound / driving**                | 앱을 호출하는 쪽 — 웹 API, CLI 등.                                  |
| **outbound / driven**                | 앱이 호출하는 쪽 — DB, 외부 API 등.                                 |
| **컴포지션 루트**                    | 구체 구현을 조립해 꽂는 단 한 곳. 여기선 `dependencies.py`.         |
| **Protocol**                         | 파이썬의 "구조적 인터페이스". 상속 없이 메서드 모양만 맞으면 만족.  |

막히면 README 의 표나 이 문서 3·5·8장을 다시 본다. 끝.
