# MMS Backup Restore

This is a Docker image which allows you to restore a backup from the MMS Backup service to a standalone instance.

## Running

You need to set enviroment variables 

 - MMS_USERNAME
 - MMS_API_KEY
 - MMS_GROUP_ID
 - MMS_CLUSTER_ID

 - MONGO_HOSTNAME

Then run

    docker run state/mms-backup-restore:latest
