FROM python:3.11.6-slim

WORKDIR /

RUN pip install --no-cache-dir fastapi[all] psycopg2 sqlalchemy alembic

COPY . .

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
