# 새 프로젝트를 클론한 직후 1회 실행하는 부트스트랩.
# 사용: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
$ErrorActionPreference = "Stop"

Write-Host "1/4  의존성 설치 (uv sync) ..." -ForegroundColor Cyan
uv sync

Write-Host "2/4  pre-commit 훅 설치 ..." -ForegroundColor Cyan
uv run pre-commit install

Write-Host "3/4  .env 준비 ..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "     .env 생성됨"
} else {
    Write-Host "     .env 이미 있음 — 건너뜀"
}

Write-Host "4/4  테스트로 환경 확인 ..." -ForegroundColor Cyan
uv run pytest -q

Write-Host "`n완료! 앱 실행:  uv run fastapi dev app/main.py  ->  http://127.0.0.1:8000/docs" -ForegroundColor Green
