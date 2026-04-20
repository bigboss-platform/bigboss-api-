install:
	poetry install

migrate:
	poetry run alembic upgrade head

seed:
	poetry run python scripts/seed.py

dev:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

setup: migrate seed

test:
	poetry run pytest tests/unit -v

test-integration:
	poetry run pytest tests/integration -v
