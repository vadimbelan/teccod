.PHONY: help run lint format typecheck test build up down logs pre-commit-install hooks

help:
	@echo "Доступные команды:"
	@echo "  make run        - запустить FastAPI локально (uvicorn)"
	@echo "  make lint       - flake8"
	@echo "  make format     - black форматирование"
	@echo "  make typecheck  - mypy"
	@echo "  make test       - pytest"
	@echo "  make build      - docker compose build web"
	@echo "  make up         - docker compose up -d web"
	@echo "  make down       - docker compose down"
	@echo "  make logs       - docker compose logs -f web"
	@echo "  make hooks      - прогнать pre-commit на всём репо"
	@echo "  make pre-commit-install - установить pre-commit хуки"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	flake8 app tests

format:
	black app tests

typecheck:
	mypy app

test:
	pytest -q

build:
	docker compose build web

up:
	docker compose up -d web

down:
	docker compose down

logs:
	docker compose logs -f web

pre-commit-install:
	pip install -r requirements-dev.txt
	pre-commit install

hooks:
	pre-commit run --all-files
