FROM python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME='/usr/local' \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

ENV POETRY_VERSION=1.2.2

RUN apt-get update; \
    apt-get install -y curl make build-essential libpq-dev gcc ffmpeg libsm6 libxext6;
RUN curl -sSL https://install.python-poetry.org | python3 -

USER root

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root

COPY . .