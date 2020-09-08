from fuzzywuzzy import fuzz
import os.path


def load_names():
    result = []
    with open("../data/names_numbers.txt") as f:
        for line in f:
            (first, last, sn) = line.strip().split("\t")
            combined_name = first + "_" + last
            result.append((combined_name, sn))

    return result

    return [("Foo_Bar", "1000"),
            ("Blatz_Blah", "2000")
            ]

def load_filenames():
    result = []
    with open("../data/filenames.txt") as f:
        for line in f:
            result.append(line.strip())
    return result

def rootname(filename):
    return os.path.splitext(filename)[0]

def match(names, name):
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
