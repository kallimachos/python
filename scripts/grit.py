#!/bin/python3
# coding: utf-8

"""Fetch latest reviews from watched OpenStack projects."""

import json
import logging
from os import path

import requests

HOST = "https://review.openstack.org/a/"
ENDPOINT = "changes/"
QUERY = "?q=status:open+is:watched&n=10"
FORMAT = "Accept: application/json"
KEYFILE = path.expanduser("~/scripts/python/scripts/grit.key")

# ----------------------------------------------------------
# CLI colours:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    WARNING = '\033[93m'
#    FAIL = '\033[91m'
#    ENDCOLOR = '\033[0m'
# ----------------------------------------------------------


def fetchkey():
    """Fetch key from file."""
    try:
        with open(KEYFILE, "rb") as f:
            logging.debug("Open " + KEYFILE)
            key = f.read()
            logging.info("Key fetched")
    except IOError as ioerr:
        logging.error("File error (fetchkey): " + str(ioerr))
        exit(1)
    return key


if __name__ == "__main__":
    user, key = fetchkey().split(":")
    url = HOST + ENDPOINT + QUERY  # + ' ' + FORMAT
    try:
        r = requests.get(url, verify=True, auth=requests.auth.HTTPDigestAuth(user, key))
        logging.debug("Content of request: " + r.text)
    except Exception as e:
        logging.error(e)
        response = input("\nWebsite error\n")
        exit(0)
    logging.info("Loading json")
    try:
        text = r.text[4:]
        print(text)
        data = json.loads(text)
        print(data)
    except Exception as e:
        logging.error(e)
        print("JSON decode error. See log.")
        exit(0)
    # do something with the decoded json here
