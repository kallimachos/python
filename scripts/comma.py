#!/bin/python3
# coding: utf-8

"""Create CSV from a list of items."""

import logging
from os import path


def readfile(infile):
    """Read data from file and return string."""
    infile = path.realpath(infile)
    try:
        with open(infile, "r") as f:
            data = f.readlines()
    except IOError as ioerr:
        logging.error("File error (readData): " + str(ioerr))
    return data


def writefile(outfile, data):
    """Write data to file."""
    outfile = path.realpath(outfile)
    try:
        with open(outfile, "w") as f:
            f.write(data)
    except IOError as ioerr:
        logging.error("File error (writeData): " + str(ioerr))


if __name__ == "__main__":
    data = readfile("temp.txt")
    new = []
    for item in data:
        new.append(item.strip())
    count = 0
    result = []
    for item in new:
        if count == 5:
            result.append(item + "\n")
            count = 0
        else:
            result.append(item + ",")
            count += 1
    result = " ".join(result)
    print(result)
