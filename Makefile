.PHONY: help run lint test build up down logs

help:
	@echo "Доступные команды:"
	@echo "  make run     - запустить FastAPI локально (uvicorn)"
	@echo "  make lint    - проверить код flake8"
	@echo "  make test    - запустить pytest"
	@echo "  make build   - собрать docker-образ"
	@echo "  make up      - поднять сервисы через docker compose"
	@echo "  make down    - остановить сервисы"
	@echo "  make logs    - показать логи web"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	flake8 app tests

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
