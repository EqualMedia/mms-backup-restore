#!/usr/bin/env python3
import http.client as http_client
import json
import logging
import os
import requests
import time
from datetime import datetime, timedelta
from requests.auth import HTTPDigestAuth
from subprocess import call
from urllib.parse import urljoin

BASE_URL = "https://mms.mongodb.com/api/public/v1.0"
HEADERS = {'Content-type': 'application/json'}


def api_call(path, user, key, json_data=None):
    url = BASE_URL + path
    auth = HTTPDigestAuth(user, key)
    r = None
    if json_data:
        data = json.dumps(json_data)
        r = requests.post(url, auth=auth, headers=HEADERS, data=data)
    else:
        r = requests.get(url, auth=auth, headers=HEADERS)

    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(r.json())


def cluster_path(group_id, cluster_id):
    return "/groups/{0}/clusters/{1}".format(group_id, cluster_id)


def create_job_point_in_time(user, key, group_id, cluster_id, dt):
    path = cluster_path(group_id, cluster_id) + "/restoreJobs"
    dt_string = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    timestamp = {"timestamp": {"date": dt_string, "increment": 0}}
    r = api_call(path, user, key, timestamp)

    return r['results'][0]['id']


def get_job(user, key, group_id, cluster_id, job_id):
    prefix = cluster_path(group_id, cluster_id)
    path = prefix + "/restoreJobs/{0}".format(job_id)
    return api_call(path, user, key)


def setup_logging():
    logging.basicConfig()
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.propagate = True

    if os.environ.get('MMS_DEBUG', 'false') == 'true':
        http_client.HTTPConnection.debuglevel = 1
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log.setLevel(logging.DEBUG)


def main():
    setup_logging()

    user = os.environ['MMS_USERNAME']
    key = os.environ['MMS_API_KEY']
    group_id = os.environ['MMS_GROUP_ID']
    cluster_id = os.environ['MMS_CLUSTER_ID']

    dt = datetime.now() - timedelta(0, 3000)

    job_id = create_job_point_in_time(user, key, group_id, cluster_id, dt)

    print("Restore job id: {0!s}".format(job_id))

    url = None
    while not url:
        job = get_job(user, key, group_id, cluster_id, job_id)
        if job["statusName"] == "FINISHED":
            print("Restore job complete.")
            url = job["delivery"]["url"]
        else:
            print("Restore job in progress...")
            time.sleep(10)

    print("Fetching {0}".format(url))

    call(["curl", url, "-o", "snapshot.tar.gz"])


if __name__ == '__main__':
        main()
