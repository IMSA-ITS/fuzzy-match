"""Translate input data using a fuzzy match against reference data.

For each line in the input data we find the best matching line in the reference
data and emit the combination of those two lines, tab separated.

The input data is considered one entire line at a time (not including the line
termination characters).

Only the content up to (and not including) the first tab character is considered
for matching in the reference data.

But the entire line of matching reference data is appended to the input line,
allowing us to append any additional data columns from the reference data (kind
of the whole point).

Any cases of suspiciously low fuzzy-match scores are reported to stderr.

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
    default_minimum = 80
    parser.add_argument(
        "-m",
        "--minimum",
        type=int,
        default=default_minimum,
        help=f"minimum fuzzy score (default: {default_minimum})",
    )
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
        if score < args.minimum:
            logger.warning(f"low score: {name_to_match} -> {best}  {score}")

        print(f"{name_to_match}\t" + "\t".join(best))


if __name__ == "__main__":
    main()
