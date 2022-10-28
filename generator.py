import csv


def generator(data):
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        yield from reader
