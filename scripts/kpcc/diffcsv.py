#!/bin/python3

import argparse
import csv
import sys


def prep(filename):
    """Uppercased list of members from a CSV file.

    Args:
        filename (str): CSV file

    Return:
        dict: dict of members
    """
    with open(filename) as f:
        f = sorted(f)
        result = []
        for line in f:
            result.append(line.upper().strip())
    result = set(result)
    members = {}
    rand = 0
    for member in result:
        member = member.split(",")
        if member[0] == "":
            member[0] = "null_" + str(rand)
            rand += 1
        members[member[0]] = member[1] + " " + member[2]
    return members


def menu(args):
    """CLI menu."""
    parser = argparse.ArgumentParser(prog="diffcsv", description="KPCC member diff")
    parser.add_argument("file1", type=str, help="CSV file")
    parser.add_argument("file2", type=str, help="CSV file")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = menu(sys.argv[1:])
    file1 = prep(args.file1)
    file2 = prep(args.file2)

    print("\nMembers that are in %s but not in %s:" % (args.file1, args.file2))
    diff1 = []
    for member in file1:
        if member in file2 or file1[member] in file2.values():
            continue
        print(member, file1[member])
        diff1.append([member, file1[member]])

    print("\nMembers that are in %s but not in %s:" % (args.file2, args.file1))
    diff2 = []
    for member in file2:
        if member in file1 or file2[member] in file1.values():
            continue
        print(member, file2[member])
        diff2.append([member, file2[member]])

    with open("result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([["Email", "Name"]])
        writer.writerows(diff1)
        writer.writerows([["", ""]])
        writer.writerows(diff2)
