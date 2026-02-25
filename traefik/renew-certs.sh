#!/bin/sh

cd "$(dirname "$0")"

docker-compose run --rm certbot renew
docker-compose restart traefik
