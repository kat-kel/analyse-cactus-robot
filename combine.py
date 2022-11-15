import csv
import os

import click
from tqdm.auto import tqdm

from fieldnames import INPUT_FILE_FIELDNAMES


@click.command
@click.argument("in_directory")
def main(in_directory):

    # PREPARE PROCESS
    out_file = prepare_out_file()
    in_files = verify_in_directory(in_directory)

    cache = {}

    # LOOP THROUGH FILES
    for file in in_files:

        # MEASURE FILE
        print(f"Parsing {file}")
        print("    Measuring the length of the file...")
        with open(file, "r") as f:
            pass_reader = csv.reader(f)
            for row in pass_reader: pass
            total = pass_reader.line_num-1

        # PARSE ROW
        csv_reader = tqdm(generate_reader(file), total=total-1, desc="Concatenating")
        for row in csv_reader:
            current_normalized_url = row.get("normalized url")
            current_count = row.get("count")
            if cache.get(current_normalized_url):
                cached_count = cache[current_normalized_url]["count"]
                new_count = int(current_count) + int(cached_count)
                row.update({"count":new_count})
            cache.update({current_normalized_url:row})

    # WRITE OUTPUT
    with open(out_file, "w") as f:
        print(f"Writing output to {out_file}")
        writer = csv.DictWriter(f, fieldnames=INPUT_FILE_FIELDNAMES)
        writer.writeheader()

        cache_reader = tqdm(generate_cache(cache), total=len(cache), desc="Writing")
        for row in cache_reader:
            writer.writerow(row)
        
        

def generate_cache(cache):
    yield from cache.values()



def generate_reader(data):
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        yield from reader


def prepare_out_file():
    out_directory = "concatenated_data"
    if not os.path.isdir(out_directory):
        os.mkdir(out_directory)
    outfile = os.path.join(out_directory, f"agreg.csv")
    return outfile


def verify_in_directory(in_directory):
    try:
        assert os.path.isdir(in_directory)
        print(f"Processing files in directory {in_directory}")

    except ValueError as err:
        print(f"\n{err}\n\
            Please enter the path to a directory.\n")
        
    script_path = os.path.dirname(os.path.realpath(__file__))
    return [os.path.join(script_path, in_directory, file) for file in os.listdir(in_directory) if file.endswith(".csv")]


if __name__ == "__main__":
    main()
