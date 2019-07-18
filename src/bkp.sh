#!/bin/bash

set -e
set -x

source /home/mlincoln/db/.env

/usr/local/bin/docker-compose -f /home/mlincoln/db/docker-compose.yml --project-directory /home/mlincoln/db/ exec -t postgres pg_dumpall -U app > /home/mlincoln/bkp/bkp.sql

cd /home/mlincoln/bkp
/usr/bin/git add .
DATE=`date +%Y-%m-%d`
/usr/bin/git commit -m "incremental backup $DATE"
