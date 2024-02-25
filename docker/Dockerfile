FROM python:3.11.7-slim AS builder

RUN apt-get update && apt-get install -y \
    musl-dev \
    libpq-dev \
    gcc \
    g++ \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

ENV PATH "/opt/venv/bin:$PATH"

COPY ../requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11.7-slim AS production

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH "/opt/venv/bin:$PATH"

WORKDIR /src

COPY .. /src/

RUN mkdir ./api/staticfiles/

RUN python api/manage.py collectstatic --no-input
