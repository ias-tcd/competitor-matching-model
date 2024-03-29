#!/bin/sh

docker-compose --env-file ./.env -f docker-compose.prod.yml run --rm api python manage.py migrate
docker-compose --env-file ./.env -f docker-compose.prod.yml up -d
docker system prune -af
