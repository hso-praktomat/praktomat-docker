#!/bin/sh

createuser -DRS praktomat
psql -c "ALTER USER praktomat WITH ENCRYPTED PASSWORD 'praktomat_password';"
createdb --encoding UTF8 -O praktomat praktomat_${COMPOSE_PROJECT_NAME}
