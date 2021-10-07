compose_file := "./docker-compose.$COMPOSE_ENV.yml"

up:
    sudo docker-compose -f {{compose_file}} up -d

down:
    sudo docker-compose -f {{compose_file}} down

reup-all:
    sudo docker-compose -f {{compose_file}} up -d --force-recreate --build

reup service:
    sudo docker-compose -f {{compose_file}} up -d --force-recreate --build {{service}}

run service:
    sudo docker-compose -f {{compose_file}} run {{service}}

run-sh service:
    sudo docker-compose -f {{compose_file}} run {{service}} sh

run-bash service:
    sudo docker-compose -f {{compose_file}} run {{service}} bash

log:
    sudo docker-compose -f {{compose_file}} logs -f

db:
    sudo docker-compose -f {{compose_file}} run db bash

deps:
    cd app && poetry export -o requirements-dev.txt --dev --without-hashes
    cd app && poetry export -o requirements.txt --without-hashes

revision message:
    sudo docker-compose -f {{compose_file}} run api alembic revision --autogenerate -m "{{message}}"
    sudo chown -R mike:mike ./app/app/db

chown-revisions:
    sudo chown -R mike:mike ./app/app/db

migrate:
    sudo docker-compose -f {{compose_file}} run api alembic upgrade head

dump-db:
    sudo docker-compose -f {{compose_file}} down -v
