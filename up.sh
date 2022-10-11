#!/bin/bash

cd $(dirname $0)

docker network create praktomat

#pushd praktomat
#docker build -t praktomat .
#popd

docker-compose --env-file=java-aki.env up -d
docker-compose --env-file=prog1-aki.env up -d

cd traefik
docker-compose up -d
