#!/bin/python3
# coding: utf-8

"""Display GitHub issues across all user's repositories."""

import argparse
import json
import logging

# import requests
# from os import path


HOST = "https://api.github.com/"
FORMAT = ""
KEYFILE = "keys/bugs.json"
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


def api(auth, req):
    """Make GitHub API request."""
    # url = HOST + key + FORMAT
    # try:
    #     r = requests.get(url)
    #     logging.debug('Content of request: ' + r.text)
    # except Exception as e:
    #     logging.error(e)
    #     response = input('\nWebsite error\n')
    #     exit(0)
    # logging.debug('Attempting to load json')
    # data = (json.loads(r.text))
    # print(data)
    pass


def fetchauth():
    """Fetch authorization info from file."""
    try:
        with open(KEYFILE, "r") as f:
            logging.debug("Open " + KEYFILE)
            info = json.load(f)
            logging.info("auth info fetched: " + str(info))
        return info
    except Exception as e:
        logging.error("File error (fetchkey): " + str(e))
        return 1


def processargs(auth, args):
    """Process command line arguments and launch related action."""
    if args.user is True:
        print("User is: " + auth["user"])
    else:
        print("No request made.")


if __name__ == "__main__":
    auth = fetchauth()
    parser = argparse.ArgumentParser(
        prog="bugs",
        description="""Display GitHub issues
                                     and PRs.""",
    )
    # parser.add_argument('INPUT', type=str, nargs='+', help='RST file(s)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--user", action="store_true", help="""Show authenticated user""")
    group.add_argument(
        "-o", "--org", action="store_true", help="""Show all orgs for authenticated user"""
    )
    args = parser.parse_args()
    processargs(auth, args)
