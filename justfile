reup-dev:
    sudo docker-compose -f ./docker-compose.dev.yml up -d --force-recreate --build

run-dev:
    sudo docker-compose -f ./docker-compose.dev.yml run server bash

log-dev:
    sudo docker-compose -f ./docker-compose.dev.yml logs -f
