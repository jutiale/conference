#!/usr/bin/env bash

# Применяем миграции Alembic
poetry run alembic upgrade head

# Запускаем FastAPI
poetry run fastapi dev main.py