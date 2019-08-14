#!/bin/python3
# coding: utf-8

"""
Check ulinks in DocBook XML file or directory of XML files.

Note this only checks for a 200 response, it does not
check that the destination contains the correct content.
"""

import argparse
import logging
from glob import iglob
from os import path

import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------
# CLI colours:
HEADER = "\033[95m"
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDCOLOR = "\033[0m"
# ----------------------------------------------------------

sumall = 0


def readdata(infile):
    """Read XML from file."""
    infile = path.realpath(infile)
    try:
        with open(infile, "rb") as f:
            xml = f.read()
    except IOError as ioerr:
        logging.error("File error (readdata): " + str(ioerr))
    return xml


def checklinks(infile, count, redirects, total, verbose):
    """Display invalid links or display count of valid and invalid links."""
    soup = BeautifulSoup(readdata(infile), "html.parser")
    badlinks = []
    allcount, goodcount, badcount = 0, 0, 0

    for ulink in soup("ulink"):
        allcount += 1
        url = str(ulink).split('"')[1]
        if verbose:
            print(HEADER + path.basename(infile) + ENDCOLOR)
            print("  Checking link: " + url)
        try:
            if redirects:
                status = requests.get(url).status_code
            else:
                status = requests.head(url).status_code
            if status == requests.codes.ok:
                status = OKGREEN + str(status)
                goodcount += 1
            else:
                status = FAIL + str(status)
                badlinks.append(status + ENDCOLOR + ": " + url)
                badcount += 1
            if verbose:
                print("  Status: " + status + ENDCOLOR)
        except Exception as e:
            logging.warning(WARNING + "Warning: " + ENDCOLOR + str(e))
            pass
    if count:
        if badcount > 0:
            print(HEADER + path.basename(infile) + ENDCOLOR)
            # print("Total links: %s\n%sGood links: %s\n%sBad links: %s%s\n"
            # % (allcount,OKGREEN,goodcount,FAIL,badcount,ENDCOLOR))
            print("%sBad links: %s%s\n" % (FAIL, badcount, ENDCOLOR))
    elif total:
        pass
    elif badcount > 0 and not verbose:
        print(HEADER + path.basename(infile) + ENDCOLOR)
        for badlink in badlinks:
            print(badlink)
    global sumall
    sumall += allcount
    return badcount


def logconfig():
    """Configure logging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/bmoss/scripts/python/linkcheck/debug.log",
        filemode="w",
    )


if __name__ == "__main__":
    logconfig()
    parser = argparse.ArgumentParser(prog="linkcheck", description="Check ulinks in DocBook XML.")
    parser.add_argument("INPUT", type=str, help="XML file or directory containing XML files")
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        default=False,
        help="Print count of invalid links per file",
    )
    parser.add_argument(
        "-r",
        "--redirects",
        action="store_true",
        default=False,
        help="Follow 301 redirects and treat redirect target as link. SLOW.",
    )
    parser.add_argument(
        "-t",
        "--total",
        action="store_true",
        default=False,
        help="Print only the total number of invalid links",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output"
    )
    args = parser.parse_args()
    badtotal = 0
    print("Checking links...\n")
    if path.isfile(args.INPUT):
        badtotal = checklinks(args.INPUT, args.count, args.redirects, args.total, args.verbose)
    else:
        for filename in iglob(args.INPUT + "*.xml"):
            badtotal += checklinks(filename, args.count, args.redirects, args.total, args.verbose)
    print("\nLinks checked: " + str(sumall))
    print("Broken links: " + str(badtotal) + "\n")
