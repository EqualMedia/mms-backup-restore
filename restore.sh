#!/bin/bash
set -e

# Create and download snapshot
/opt/fetch_snapshot.py

# Extract snapshot
tar --strip-components=1 -C /data/db -zxvf snapshot.tar.gz

# Convert mongo directory snapshot into a bson dump.
mongodump --dbpath /data/db --db $MONGO_DB_NAME

# Import dump into specified mongo instance.
mongorestore -h $MONGO_HOSTNAME --db $MONGO_DB_NAME --drop dump/$MONGO_DB_NAME
