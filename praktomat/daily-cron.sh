#!/bin/bash

# Restore environment variables
while IFS== read -r key value; do
  printf -v "$key" %s "$value" && export "$key"
done < /home/praktomat/praktomat.env

python3 /home/praktomat/Praktomat/src/manage-local.py runallcheckers
