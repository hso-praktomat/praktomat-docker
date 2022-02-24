# syntax=docker/dockerfile:1
FROM postgres:14.2-alpine

ARG ID
COPY init.sh /docker-entrypoint-initdb.d/init.sh
RUN sed -i -e "s/\${id}/$ID/" /docker-entrypoint-initdb.d/init.sh
