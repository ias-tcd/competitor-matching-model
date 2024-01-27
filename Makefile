build:
	docker-compose -f docker/docker-compose.local.yml build

run:
	docker-compose -f docker/docker-compose.local.yml up --build

down:
	docker-compose -f docker/docker-compose.local.yml down

restart:
	make down && make run

format: path ?= .
format:
	isort $(path) -l 120 --multi-line=3 --trailing-comma && black $(path) --line-length 120

lint: path ?= .
lint:
	flake8 $(path) --max-line-length=120 --extend-ignore=E129,E2 --exclude=venv
