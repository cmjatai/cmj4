#!/usr/bin/env bash

echo -e "\033[38;2;255;255;0;2m\033[1m====> StartPRD...\033[0m"

#/bin/bash wait-for-pg.sh "postgresql://cmj_st1:cmj_st1@cmjdb:5432/cmj"

yes yes | python3 manage.py migrate

#rm /var/cmjatai/cmj/logs/celery/*.pid
#celery multi start 16 -A cmj -l INFO -Q:1-10 cq_arq -Q:11-12 cq_core -Q:13 cq_videos -Q:14 cq_base -Q:15-16 celery -c 2 --hostname=cmjredis --pidfile=./logs/celery/%n.pid --logfile=./logs/celery/%n%I.log

#celery multi start 1 -A cmj -l INFO -Q:1 celery -c:1 1 --hostname=cmjredis --pidfile=./logs/celery/%n.pid --logfile=./logs/celery/%n%I.log

/bin/sh start_daphne.sh &
/bin/sh start_gunicorn.sh &
/usr/sbin/nginx -g "daemon off;"
