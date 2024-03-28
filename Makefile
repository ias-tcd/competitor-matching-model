.PHONY: build run down restart migrations migrate syncdb shell startapp enter test lint format model detect-infer

build:
	docker-compose -f docker/docker-compose.local.yml build

run:
	docker-compose -f docker/docker-compose.local.yml up --build --remove-orphans

down:
	docker-compose -f docker/docker-compose.local.yml down

restart:
	make down && make run

migrations:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py makemigrations

migrate:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py migrate

syncdb:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py syncdb

shell:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py shell

startapp:
	docker-compose -f docker/docker-compose.local.yml run --rm --workdir=/src/api api python manage.py startapp $(name)

enter:
	docker-compose -f docker/docker-compose.local.yml run --rm --entrypoint=sh api

test:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py test $(if $(path),tests.$(path),tests) --keepdb

format: path ?= .
format:
	isort $(path) -l 120 --multi-line=3 --trailing-comma && black $(path) --line-length 120

lint: path ?= .
lint:
	flake8 $(path) --max-line-length=120 --extend-ignore=E129,E2 --exclude=venv

model:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py run_model $(name)

detect-infer:
	docker-compose -f docker/docker-compose.local.yml run --rm api python api/manage.py detect_and_infer $(name)
