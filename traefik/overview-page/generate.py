#!/usr/bin/python3

import os
from shell import *
import sys

instances_html = []

# Read instance template
with open(pjoin(dirname(__file__), "instance.html.in")) as f:
    instance_template = f.read()

for path in sys.argv[1:]:
    domain = "localhost"
    name = "unknown instance name"
    instance_id = ""
    with open(path) as f:
        for line in f.readlines():
            if "PRAKTOMAT_NAME" in line:
                name = line.replace("PRAKTOMAT_NAME=", "").strip()
            elif "COMPOSE_PROJECT_NAME" in line:
                instance_id = line.replace("COMPOSE_PROJECT_NAME=", "").strip()
            elif "PRAKTOMAT_DOMAIN" in line:
                domain = line.replace("PRAKTOMAT_DOMAIN=", "").strip()
    fragment = instance_template.replace("<!-- NAME -->", name).replace("<!-- ID -->", instance_id).replace("<!-- DOMAIN -->", domain)
    instances_html.append(fragment)

# Read master template
with open(pjoin(dirname(__file__), "index.html.in")) as f:
    site = f.read()
site = site.replace("<!-- INSTANCES -->", "\n".join(instances_html))
with open(pjoin(dirname(__file__), "output", "index.html"), "w") as f:
    f.write(site)
