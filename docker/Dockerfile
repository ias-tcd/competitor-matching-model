FROM python:3.11.7-alpine AS builder

RUN apk update && apk add musl-dev libpq-dev gcc

RUN python -m venv /opt/venv

ENV PATH "/opt/venv/bin:$PATH"

COPY ../requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

FROM python:3.11.7-alpine

RUN apk update && apk add libpq-dev

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH "/opt/venv/bin:$PATH"

WORKDIR /src

COPY .. /src/

RUN mkdir ./api/staticfiles/

RUN python api/manage.py collectstatic --no-input
