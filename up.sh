#!/bin/bash

cd $(dirname $0)

docker network create praktomat

#pushd praktomat
#docker build -t praktomat .
#popd

ENV_FILES=""
start_instance() {
    docker compose --env-file=$1 up -d
    ENV_FILES="$ENV_FILES $1"
}

start_instance oosd.env
start_instance adv-cpp.env
start_instance prog1-aki.env
start_instance java-aki.env
start_instance advanced-prog.env
start_instance prog-nes.env

# Regenerate overview page
python3 traefik/overview-page/generate.py $ENV_FILES

cd traefik
docker compose up -d
