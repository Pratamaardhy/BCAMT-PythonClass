.PHONY: setup run db-up migrate migrate-auto test clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/uvicorn app.main:app --reload -> jalanin server uvicorn di localhost:8000

db-up:
	docker compose up -d db

migrate-auto:
	.venv/bin/alembic revision --autogenerate -m "init"


migrate:
	.venv/bin/alembic upgrade head

test:
	.venv/scripts/python -m pytest -v

clean:
	rm -rf .venv .pytest_cache __pycache__
