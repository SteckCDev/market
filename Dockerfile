FROM python:3.11.6

WORKDIR /market

COPY . ./
COPY .dev.env .dev.env

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
