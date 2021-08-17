compose_file := ./docker-compose.$COMPOSE_ENV.yml

reup:
    sudo docker-compose -f {{compose_file}} up -d --force-recreate --build

run:
    sudo docker-compose -f {{compose_file}} run server bash

log:
    sudo docker-compose -f {{compose_file}} logs -f
