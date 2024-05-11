#!/bin/bash

cd $(dirname $0)

docker network create praktomat

#pushd praktomat
#docker build -t praktomat .
#popd

ENV_FILES=""
start_instance() {
    docker-compose --env-file=$1 up -d
    ENV_FILES="$ENV_FILES $1"
}

start_instance aud-ai.env
start_instance aud-win.env
start_instance prog2-aki.env

# Regenerate overview page
python3 traefik/overview-page/generate.py $ENV_FILES

cd traefik
docker-compose up -d
