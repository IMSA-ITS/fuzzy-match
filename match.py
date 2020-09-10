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
    """ Read tab-separated data and return its content as list of lists. """
    return [line.strip().split("\t") for line in f]


def match(names, name):
    """ Return the best match of `name` from the list of `names` """
    # print(f"match({name})")

    best_score = 0
    best_match = ""
    for n in names:
        name_test = n[0]
        score = fuzz.ratio(name, name_test)
        # logger.debug(f"score of {name} against {name_test} is {score}")

        if score > best_score:
            best_score = score
            best_match = n

        if score == 100:
            # Can't get better than this, so save time by stopping the search
            break

    return (best_match, best_score)


def main():
    parser = argparse.ArgumentParser(description="Find best fuzzy matches")
    parser.add_argument("matchfile", help="file with values to match")
    parser.add_argument("-d", "--debug", action="store_true", help="log debug messages")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    logger.debug(f"args = {args}")

    with open(args.matchfile) as f:
        names = load_names(f)

    infile = sys.stdin
    for line in infile:
        name_to_match = line.strip()
        (best, score) = match(names, name_to_match)
        logger.debug(f"{name_to_match} -> {best}  {score}")
        if score < 80:
            logger.warning(f"low score: {name_to_match} -> {best}  {score}")

        print(f"{name_to_match}\t" + "\t".join(best))


if __name__ == "__main__":
    main()
