#!/bin/bash

cd $(dirname $0)

docker network create praktomat

#pushd praktomat
#docker build -t praktomat .
#popd

docker-compose --env-file=aud-ai.env up -d
docker-compose --env-file=aud-win.env up -d
docker-compose --env-file=prog2-aki.env up -d

cd traefik
docker-compose up -d
