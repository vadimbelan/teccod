# TECCOD Test Task

![CI](https://github.com/vadimbelan/teccod/actions/workflows/ci.yml/badge.svg)

Мини-демо сервис поиска документов в OpenSearch с веб-интерфейсом на FastAPI.

## Возможности
- Индекс `documents` со схемой:
  - `title` — `text`
  - `content` — `text`
  - `content_type` — `keyword` (допустимые значения: `article`, `blog`, `news`, `report`)
- Сидинг 5 демо-документов
- Поиск `multi_match` по `title` + `content` с `term`-фильтром по `content_type`
- API (`/init_index`, `/seed`, `/search`, `/os_health`, `/health`) и простой UI (`/ui`)

## Быстрый старт
> Требуется Docker Compose.

```bash
# 0) Запустить OpenSearch
docker compose up -d --build web

# 1) Проверка статусов
docker compose ps

# 2) Проверить приложения
curl -s http://localhost:8000/health
curl -s http://localhost:9200

# 3) (если индекс пуст) Инициализация и сидинг
curl -s -X POST http://localhost:8000/init_index | python -m json.tool
curl -s -X POST http://localhost:8000/seed | python -m json.tool

# 4) UI
# Открыть в браузере:
# http://localhost:8000/ui
```

# Порты по умолчанию

- **Web (FastAPI):** [http://localhost:8000](http://localhost:8000)  
- **OpenSearch API:** [http://localhost:9200](http://localhost:9200)  
- **OpenSearch Dashboards (опционально):** [http://localhost:5601](http://localhost:5601)  

Запускается профилем:
```bash
docker compose --profile dashboards up -d dashboards
```

# Локальная разработка без Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Если OpenSearch в Docker, поставьте OS_HOST=localhost в .env:
# OS_HOST=localhost

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# затем:
curl -s -X POST http://localhost:8000/init_index | python -m json.tool
curl -s -X POST http://localhost:8000/seed | python -m json.tool
```

# Описание API

- **GET `/health`** — статус веб-приложения  
- **GET `/os_health`** — краткий статус кластера OpenSearch  
- **POST `/init_index`** — создаёт индекс (идемпотентно)  
- **POST `/seed`** — загружает 5 демо-документов  
- **GET `/search?q=...&content_type=...`** — поиск с опциональным фильтром  

# Примеры

```bash
curl -s "http://localhost:8000/search?q=FastAPI" | python -m json.tool

curl -s "http://localhost:8000/search?q=Docker&content_type=blog" | python -m json.tool

curl -s "http://localhost:8000/search?q=OpenSearch&content_type=news" | python -m json.tool
```

# Веб-интерфейс

**GET /ui** — форма с:  
- текстовым полем `q`  
- переключателями `content_type` (`any` / `article` / `blog` / `news` / `report`)  

Результаты показываются как список:  
- `title`  
- `snippet` (первые 50 символов `content`)

# Тесты

Интеграционные тесты (ожидают работающий API и сидинг):

```bash
pytest -q -k search_examples
```

# ⚠️ Текущие настройки предназначены **только для DEV**:

- Security Plugin OpenSearch отключён.  
- Подключение к OpenSearch — по HTTP без аутентификации/SSL.  
