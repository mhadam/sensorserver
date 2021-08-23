compose_file := "./docker-compose.$COMPOSE_ENV.yml"

up:
    sudo docker-compose -f {{compose_file}} up -d

reup:
    sudo docker-compose -f {{compose_file}} up -d --force-recreate --build

run:
    sudo docker-compose -f {{compose_file}} run server bash

log:
    sudo docker-compose -f {{compose_file}} logs -f

db:
    sudo docker-compose -f {{compose_file}} run db bash

deps:
    cd app && poetry export -o requirements-dev.txt --dev --without-hashes
    cd app && poetry export -o requirements.txt --without-hashes
