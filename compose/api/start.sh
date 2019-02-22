#!/usr/bin/env bash

export CPU_COUNT=`grep -c ^processor /proc/cpuinfo `
export WORKER_COUNT=${WORKER_COUNT:-$(( $CPU_COUNT * 2 ))}
export MAX_REQUESTS=${MAX_REQUESTS:-1000}

[ ! -z $ENV_FILE ] \
    && source ${ENV_FILE}.env
env

./manage.py migrate \
    || { echo >&2 "[CRIT] migrate fails. Aborting"; exit 1; }

gunicorn --bind 0.0.0.0:8000 -k eventlet -w $WORKER_COUNT --max-requests $MAX_REQUESTS --reload myproject.wsgi:application
