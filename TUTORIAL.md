# TUTORIAL — 폴더 구조 설명

각 폴더가 뭔지, 요청이 어떻게 흐르는지, 새 기능을 어디에 넣는지, 팀으로 어떻게 같이 작업하는지를 담았다.
예제로 "주문(Order)"이 이미 들어 있으니 따라가며 보면 된다.

---

## 1. 한 줄 요약

바깥(웹·DB)과 안쪽(비즈니스 로직)을 분리하고, 그 사이를 포트(계약)로 잇는다.
→ DB 없이도 로직을 만들고 테스트할 수 있고, 나중에 DB를 갈아끼워도 안쪽 코드는 안 바뀐다.

이걸 헥사고날 아키텍처(포트 & 어댑터)라 부른다. 이 템플릿은 해커톤용으로 꼭 필요한 만큼만 남긴 경량 버전.

---

## 2. 비유 — 컴퓨터

- 본체 = 핵심 로직(domain + application). 계산만 한다. 입력이 어디서 오든, 출력이 어디로 가든 신경 안 쓴다.
- USB·HDMI 구멍 = 포트(ports). "이 규격이면 뭐든 OK"라는 약속.
- 주변기기 = 어댑터(adapters).
  - 키보드·마우스 = inbound(들어오는 쪽). 본체에 입력을 넣는다.
  - 모니터·프린터 = outbound(나가는 쪽). 본체에서 결과를 빼낸다.

핵심: 규격(포트)만 맞으면 어떤 기기를 꽂아도 본체는 그대로다. 그게 이 구조의 최고 장점.

---

## 3. 단 하나의 규칙 (THE ONE RULE)

import는 항상 안쪽으로만 향한다.

```
바깥 ──────────────────▶ 안쪽
adapters   →   application   →   domain

✅ 바깥이 안쪽을 import     (OK)
❌ 안쪽이 바깥을 import     (금지 — domain이 fastapi를? 절대 안 됨)
```

파일이 어디 속하는지 판별법:

- fastapi 를 import → inbound 어댑터 (adapters/inbound/)
- sqlalchemy·httpx 를 import → outbound 어댑터 (adapters/outbound/)
- 둘 다 아니면 → domain 또는 application

사람이 깜빡해도 CI가 잡는다 (`uv run lint-imports`). 어기면 PR이 빨갛게 뜬다.

---

## 4. 폴더 지도

```text
app/                    # 실제 코드. 열면 바로 구조가 보인다
├── main.py             # 진입점: 앱을 만들고 라우터를 끼운다
├── dependencies.py     # 조립소: 어떤 구현을 꽂을지 정하는 유일한 곳
├── domain/             # 가장 안쪽. 순수 규칙. 프레임워크 import 금지
│   ├── models.py       #   데이터 + 규칙 (예: Order)
│   └── errors.py       #   비즈니스 예외 (예: OrderNotFound)
├── application/        # 할 일(유스케이스). domain·포트만 안다
│   ├── ports.py        #   포트(계약): "저장소는 이런 모양"이라는 약속
│   └── services.py     #   OrderService: 주문 넣기/조회 등 시나리오
├── adapters/           # 바깥세상 연결. 안쪽을 import (반대 금지)
│   ├── inbound/api/    #   들어오는 쪽: routers.py(웹 입구) + schemas.py(요청·응답 모양)
│   └── outbound/       #   나가는 쪽: memory.py(저장소 구현)
└── infrastructure/     # 얇은 기술 계층: settings.py(설정 읽기)

tests/                  # app을 거울처럼 따라감 (unit / api)
```

(루트엔 pyproject.toml·uv.lock·README.md 등 설정·문서 파일. 자세한 건 README 참고.)

---

## 5. 이거 추가하려면 어디?

| 추가할 것 | 어디 |
|---|---|
| 비즈니스 규칙·계산 | domain/models.py 또는 application/services.py |
| 새 HTTP 엔드포인트 | adapters/inbound/api/routers.py (+ schemas.py) |
| 저장·외부 연동 | adapters/outbound/ |
| 구현 교체 (메모리→DB) | dependencies.py 한 줄 |
| 설정값 | infrastructure/settings.py |

포트의 위력: 메모리를 진짜 DB로 바꿔도 dependencies.py의 `get_repository` 한 줄만 고치면 끝. services·routers·domain은 그대로다.

---

## 6. 요청이 흐르는 길 (POST /orders)

```
routers.py (요청 받음)
  → services.py (주문 만들기 시나리오)
    → domain (Order 생성, 규칙 적용)
    → 포트로 "저장해줘"
      → outbound/memory.py (실제 저장)
  → 결과를 OrderResponse로 바꿔 201 응답
```

핵심: 가운데(services·domain)는 메모리인지 DB인지 모른다. 그래서 저장 방식만 바꿔도 로직은 그대로.

---

## 7. 팀으로 같이 작업하기

- GitHub 레포 = 팀의 공유 원본 한 부(main). 아무나 동시에 막 고치는 게 아니라 "제안 → 리뷰 → 합치기" 방식.
- clone = 각자 노트북에 내 사본 받기.
- branch(브랜치) = 원본을 안 건드리고 만드는 내 작업 칸막이.
- Pull Request(PR) = "내 칸에서 한 거, 원본에 합쳐주세요" 하는 제안서 → 팀원이 보고 OK하면 main에 들어감.

하루 흐름:

```
① main 최신 받기 (git pull)
② 내 브랜치 만들기
③ 만들고 commit · push
④ PR 올려 팀원 1명 리뷰
⑤ main에 머지 → 반복
```

이 폴더 구조 덕에 각자 다른 폴더를 맡으면(누구는 adapters, 누구는 domain) 같은 파일을 거의 안 건드려서 충돌이 적다. (브랜치·커밋 규칙은 CONTRIBUTING.md)

---

## 8. 명령어 (외울 건 이것뿐)

| 하고 싶은 것 | 명령 |
|---|---|
| 처음 세팅 | `uv sync` → `Copy-Item .env.example .env` → `uv run pre-commit install` |
| 앱 실행 | `uv run fastapi dev app/main.py` (→ `/docs`) |
| 테스트 | `uv run pytest` |
| 포맷·린트 | `uv run ruff format .` / `uv run ruff check .` |
| 타입 검사 | `uv run mypy` |
| 규칙 검사 | `uv run lint-imports` |
| 패키지 추가 | `uv add <이름>` (→ uv.lock 자동 갱신 → 커밋) |

왜 전부 `uv run`? uv가 uv.lock에 잠긴 정확한 버전으로 실행해주기 때문. 그래서 5명 결과가 항상 같다.
`pip install`이나 `python xxx.py`를 직접 쓰면 잠금이 깨져 "내 컴퓨터에선 됐는데"가 시작된다.

---

## 9. 하면 안 되는 것

- domain·application 안에서 fastapi·sqlalchemy import → 규칙 위반(CI가 막음)
- routers에 비즈니스 로직 작성 → routers는 받아서 넘기기만, 계산은 services·domain
- 저장소를 routers에서 직접 생성 → 조립은 dependencies.py에서만 (안 그러면 테스트에서 교체 불가)
- pip install / python -m venv → uv add · uv sync · uv run 만
- .env 커밋 / uv.lock 무시 → 반대로 해야 함 (.env는 비밀이라 금지, uv.lock은 꼭 커밋)

---

## 용어

| 용어 | 뜻 |
|---|---|
| 포트(port) | "이런 모양이어야 한다"는 약속. 여기선 OrderRepository |
| 어댑터(adapter) | 포트에 꽂히는 실제 구현. inbound(입력)·outbound(저장 등) |
| 컴포지션 루트 | 구현을 골라 꽂는 단 한 곳. 여기선 dependencies.py |
| Protocol | 상속 없이 메서드 모양만 맞으면 인정되는 파이썬 인터페이스 |
