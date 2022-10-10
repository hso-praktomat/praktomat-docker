#!/bin/bash

$(dirname $0)/run-tivoli-client dsmc query backup '/data/*'  -subdir=yes
