#!/usr/bin/env bash

poetry run alembic upgrade head
poetry run fastapi dev main.py --host 0.0.0.0 --port 8000
