#!/usr/bin/env bash

echo -e "\033[38;2;255;255;0;2m\033[1m====> StartDEV...\033[0m"

sed -i -E "s/^DEBUG.+$/DEBUG = ${DEBUG:=True}/g" cmj4/.env

yes yes | python3 manage.py migrate


## SOLR
USE_SOLR="${USE_SOLR:=False}"
SOLR_URL="${SOLR_URL:=http://solr:solr@cmj4solr:8983}"
SOLR_COLLECTIONS="${SOLR_COLLECTIONS:=portalcmj4_cmj}"
NUM_SHARDS=${NUM_SHARDS:=1}
RF=${RF:=1}
MAX_SHARDS_PER_NODE=${MAX_SHARDS_PER_NODE:=1}
IS_ZK_EMBEDDED="${IS_ZK_EMBEDDED:=True}"

if [ "${USE_SOLR-False}" == "True" ] || [ "${USE_SOLR-False}" == "true" ]; then

    echo "Solr configurations"
    echo "==================="
    echo "URL: $SOLR_URL"
    echo "COLLECTION: $SOLR_COLLECTIONS"
    echo "NUM_SHARDS: $NUM_SHARDS"
    echo "REPLICATION FACTOR: $RF"
    echo "MAX SHARDS PER NODE: $MAX_SHARDS_PER_NODE"
    echo "ASSUME ZK EMBEDDED: $IS_ZK_EMBEDDED"
    echo "========================================="

    echo "running Solr script"
    /bin/bash _docker/prod/wait-for-solr.sh $SOLR_URL
    CHECK_SOLR_RETURN=$?

    if [ $CHECK_SOLR_RETURN == 1 ]; then
        echo "Connecting to Solr..."

        if [ "${IS_ZK_EMBEDDED-False}" == "True" ] || [ "${IS_ZK_EMBEDDED-False}" == "true" ]; then
            ZK_EMBEDDED="--embedded_zk"
            echo "Assuming embedded ZooKeeper instalation..."
        fi

        python3 _docker/prod/solr_cli.py -u $SOLR_URL -c $SOLR_COLLECTIONS -s $NUM_SHARDS -rf $RF -ms $MAX_SHARDS_PER_NODE $ZK_EMBEDDED

    else
        echo "Solr is offline, not possible to connect."
    fi

else
    echo "Solr support is not initialized."
fi

rm /var/cmjatai/cmj4/logs/celery/*.pid
celery multi start 5 -A cmj4 -l INFO -Q:1 cq_arq -Q:2 cq_core -Q:3 cq_videos -Q:4 cq_base -Q:5 celery -c 2 --hostname=cmj4redis --pidfile=./logs/celery/%n.pid --logfile=./logs/celery/%n%I.log

yes yes | python3 manage.py runserver 0.0.0.0:9000