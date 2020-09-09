"""
Generate mapping file needed to upload photos to PowerSchool.
"""

from fuzzywuzzy import fuzz
import os.path


def load_names():
    """ Return list of (name, student_number) tuples based on data from PowerSchool. """
    result = []
    with open("../data/names_numbers.txt") as f:
        for line in f:
            (first, last, sn) = line.strip().split("\t")
            combined_name = first + "_" + last
            result.append((combined_name, sn))

    return result

def load_filenames():
    """ Return list of all the image filenames. """
    result = []
    with open("../data/filenames.txt") as f:
        for line in f:
            result.append(line.strip())
    return result

def rootname(filename):
    """ Map filename to its base without extension.
    E.g. rootname("foo.png") -> "foo"

    """
    return os.path.splitext(filename)[0]

def match(names, name):
    """ Return the best match of `name` from the list of `names` """
    #print(f"match({name})")
    scores = [(fuzz.ratio(name, n[0]), n) for n in names]
    #print(f"scores = {scores}")
    best = sorted(scores, key=lambda t: t[0], reverse=True)[0]

    return best


if __name__ == "__main__":
    names = load_names()

    filenames = load_filenames()

    for filename in filenames:
        root = rootname(filename)
        matched = match(names, root)

        print(f"{filename} -> {matched}")
