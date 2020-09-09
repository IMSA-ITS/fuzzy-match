"""
Generate mapping file needed to upload photos to PowerSchool.
"""

import argparse
import logging
from fuzzywuzzy import fuzz
import os.path
import sys


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("match")


def load_names(f):
    """ Return list of (name, value) tuples. """
    return [line.strip() for line in f]


def match(names, name):
    """ Return the best match of `name` from the list of `names` """
    # print(f"match({name})")

    best_score = 0
    best_name = ""
    for n in names:
        score = fuzz.ratio(name, n)
        # logger.debug(f"score of {name} against {n} is {score}")

        if score > best_score:
            best_score = score
            best_name = n

        if score == 100:
            break

    return (best_name, best_score)


def main():
    parser = argparse.ArgumentParser(description="Find best fuzzy matches")
    parser.add_argument("matchfile", help="file with values to match")
    parser.add_argument("-d", "--debug", action="store_true", help="log debug messages")
    args = parser.parse_args()
    logger.debug(f"args = {args}")

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    with open(args.matchfile) as f:
        names = load_names(f)

    infile = sys.stdin
    for line in infile:
        name_to_match = line.strip()
        (best, score) = match(names, name_to_match)
        logger.debug(f"{name_to_match} -> {best}  {score}")
        if score < 90:
            logger.warning(f"low score: {name_to_match} -> {best}  {score}")

        print(f"{name_to_match}\t{best}")


if __name__ == "__main__":
    main()
