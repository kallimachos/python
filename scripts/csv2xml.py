#!/bin/python3
# coding: utf-8

"""
Create a Docbook XML table from a CSV file.

CSV file must be encoded in ASCII or UTF-8.
"""

import argparse
import csv
import logging
import re
from os import path

from bs4 import BeautifulSoup

# Hack to set the indent for prettify
orig_prettify = BeautifulSoup.prettify
r = re.compile(r"^(\s*)", re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    """Set indent for prettify."""
    return r.sub(r"\1" * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def readcsv(infile):
    """Read CSV from file and return a matrix of rows."""
    infile = path.realpath(infile)
    matrix = []
    try:
        with open(infile, "rb") as f:
            reader = csv.reader(f)
            for row in reader:
                matrix.append(row)
    except IOError as ioerr:
        logging.error("File error (readData): " + str(ioerr))
    return matrix


def writexml(outfile, xml):
    """Write an XML string to file."""
    outfile = path.realpath(outfile)
    try:
        with open(outfile, "wb") as f:
            f.write(xml)
        print("XML saved to " + outfile)
    except IOError as ioerr:
        logging.error("File error (writeData): " + str(ioerr))


def createrow(row_list):
    """Create an XML <row> from the entries in row_list."""
    soup = BeautifulSoup("<row></row>", "xml")
    for cell in row_list:
        entry = soup.new_tag("entry")
        entry.string = cell
        soup.row.append(entry)
    return soup.row


def buildtable(matrix, section):
    """Return an XML <informaltable> built from a matrix of rows."""
    if section is True:
        soup = BeautifulSoup(
            """<section>
                                    <title>Insert Title Here</title>
                                    <informaltable>
                                        <tgroup>
                                        </tgroup>
                                    </informaltable>
                                </section>""",
            "xml",
        )
    else:
        soup = BeautifulSoup(
            """<informaltable>
                                    <tgroup>
                                    </tgroup>
                                </informaltable>""",
            "xml",
        )

    # tgroup
    # cols = 'cols="' + str(len(matrix[1])) + '"'
    soup.tgroup["cols"] = str(len(matrix[1]))

    # thead
    thead = soup.new_tag("thead")
    soup.tgroup.append(thead)
    header = matrix.pop(0)
    thead.append(createrow(header))

    # tbody
    tbody = soup.new_tag("tbody")
    soup.tgroup.append(tbody)
    for row in matrix:
        tbody.append(createrow(row))

    return soup.prettify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="csv2xml", description="""Creates a Docbook XML table from a CSV file"""
    )
    parser.add_argument("INPUT", type=str, help="CSV file")
    parser.add_argument("OUTPUT", type=str, nargs="?", default=None, help="XML file")
    parser.add_argument(
        "-s", "--section", action="store_true", default=False, help="Add section tags"
    )
    args = parser.parse_args()
    print("Generating table...\n")
    table = buildtable(readcsv(args.INPUT), args.section)
    if args.OUTPUT is not None:
        writexml(args.OUTPUT, table)
    else:
        print(table + "\nTable complete.")
