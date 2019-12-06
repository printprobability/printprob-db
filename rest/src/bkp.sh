#!/bin/bash

set -e
set -x

source /vol/pp/.env

/usr/local/bin/docker-compose -f /vol/pp/docker-compose.yml --project-directory /vol/pp/ exec -T postgres pg_dumpall -U app > /vol/bkp/bkp.sql

cd /vol/bkp
/usr/bin/git add .
DATE=`date +%Y-%m-%d`
/usr/bin/git commit -m "incremental backup $DATE"
