# syntax=docker/dockerfile:1

FROM python:3.13

ENV POETRY_HOME="/usr/local"
ENV POETRY_VERSION=2.0.1
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /api
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY entrypoint.sh .
COPY api ./api
COPY main.py .
COPY alembic ./alembic
COPY alembic.ini .


RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]



