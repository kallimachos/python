#!/bin/python3
# coding: utf-8

"""Display status of sites monitored by Uptimerobot on the command line."""

import json
import logging
from os import path

import requests

HOST = "http://api.uptimerobot.com/getMonitors?apikey="
FORMAT = "&format=json&noJsonCallback=1"
KEYFILE = path.expanduser("~/scripts/python/scripts/uptime.key")
status_code = {
    "0": "\033[94mpaused",
    "1": "not checked yet",
    "2": "\033[92mup",
    "8": "\033[93mseems down",
    "9": "\033[91mdown",
}

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
    """Fetch API key from file."""
    try:
        with open(KEYFILE, "rb") as f:
            logging.debug("Open " + KEYFILE)
            key = f.read()
            logging.info("key fetched")
    except IOError as ioerr:
        logging.error("File error (fetchkey): " + str(ioerr))
        exit(1)
    return key


if __name__ == "__main__":
    key = fetchkey()
    url = HOST + key + FORMAT
    try:
        r = requests.get(url)
        logging.debug("Content of request: " + r.text)
    except Exception as e:
        logging.error(e)
        response = input("\nWebsite error\n")
        exit(0)
    logging.debug("Attempting to load json")
    data = json.loads(r.text)
    print("")
    for monitor in data["monitors"]["monitor"]:
        print("%s %s%\033[0m %s") % (
            status_code[monitor["status"]],
            monitor["alltimeuptimeratio"],
            monitor["friendlyname"],
        )
    print("")
