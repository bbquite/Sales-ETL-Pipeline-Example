FROM apache/superset:latest

USER root

# Устанавливаем psycopg2 прямо в виртуальное окружение Superset
RUN python3 -m venv /app/.venv \
    && /app/.venv/bin/pip install --upgrade pip \
    && /app/.venv/bin/pip install psycopg2-binary

USER superset