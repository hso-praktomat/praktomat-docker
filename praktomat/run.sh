#!/bin/sh

./wait-for-it.sh postgresql:5432

python3 Praktomat/src/manage-local.py migrate --noinput && \
sudo -E apache2ctl -DFOREGROUND
