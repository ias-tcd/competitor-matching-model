build:
	docker-compose -f docker/docker-compose.local.yml build

run:
	docker-compose -f docker/docker-compose.local.yml up --build

down:
	docker-compose -f docker/docker-compose.local.yml down

restart:
	make down && make run

migrations:
	docker-compose -f docker/docker-compose.local.yml run api python api/manage.py makemigrations

migrate:
	docker-compose -f docker/docker-compose.local.yml run api python api/manage.py migrate

syncdb:
	docker-compose -f docker/docker-compose.local.yml run api python api/manage.py syncdb

shell:
	docker-compose -f docker/docker-compose.local.yml run api python api/manage.py shell

startapp:
	docker-compose -f docker/docker-compose.local.yml run --workdir=/src/api api python manage.py startapp $(name)

enter:
	docker-compose -f docker/docker-compose.local.yml run --entrypoint=sh api

test:
	docker-compose -f docker/docker-compose.local.yml run api python api/manage.py test $(if $(path),tests.$(path),tests) --keepdb

format: path ?= .
format:
	isort $(path) -l 120 --multi-line=3 --trailing-comma && black $(path) --line-length 120

lint: path ?= .
lint:
	flake8 $(path) --max-line-length=120 --extend-ignore=E129,E2 --exclude=venv
