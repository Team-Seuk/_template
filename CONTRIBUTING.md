# 협업 규칙 (CONTRIBUTING)

5명이 한 레포에서 부딪히지 않고 빠르게 일하기 위한 최소 규칙. 매 프로젝트 동일하다.

## 작업 흐름 (GitHub Flow, 6단계)

```powershell
# 1. 최신 main 받기
git switch main
git pull

# 2. 짧은 작업 브랜치 만들기
git switch -c feat/내이름-기능요약        # 예: feat/seuk-order-api

# 3. 코드 짜고, 작게 자주 커밋
git add -A
git commit -m "feat: 주문 생성 API 추가"   # 커밋 메시지 규칙은 아래

# 4. 올리기
git push -u origin feat/내이름-기능요약

# 5. GitHub 에서 Pull Request 열기 → 팀원 1명 승인(approve)

# 6. Squash merge → 브랜치 삭제. 끝.
```

> 직접 `main` 에 push 하지 않는다(보호되어 있음). 항상 브랜치 → PR.

## 브랜치 이름
`<종류>/<내이름>-<요약>` — 종류: `feat`(기능) · `fix`(버그) · `chore`(잡일) · `docs`(문서)
예: `feat/seuk-login`, `fix/jin-null-error`

## 커밋 메시지 (Conventional Commits)
`<종류>: <한 줄 요약>` — 예: `feat: 로그인 엔드포인트 추가`, `fix: 주문 금액 음수 방지`

## PR 규칙
- **작게.** 한 PR = 한 가지 일. 리뷰어가 5분 안에 볼 수 있게.
- 머지 전 체크: `uv run pytest` · `uv run ruff check .` · `uv run mypy` 통과(CI가 자동 확인).
- 리뷰 1명 승인이면 머지. 해커톤 중엔 옆자리에 "리뷰 좀" 하면 30초다.

## 코드 규칙
- **THE ONE RULE**(README 참고)을 어기지 않는다. `domain/`·`application/` 안에서 `fastapi`/`sqlalchemy` 를 import 하면 CI 가 막는다.
- 의존성은 `uv add` 로만 추가하고 `uv.lock` 을 함께 커밋한다.
