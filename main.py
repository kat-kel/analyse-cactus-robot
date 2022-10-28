import os

import click

from parseCSV import parse_csv
from output import writer


@click.command
@click.argument("csv")
@click.argument("count")
def main(csv, count):

    if os.path.isfile(csv):

        title = "enriched_"+os.path.basename(csv)

        try:
            int(count)
            results, counters = parse_csv(csv,count) # add something to do with aggregated counts
            print("Writing output")
            writer(results, title)

        except ValueError as err:
            print(f"\n{err}\n\
                Please enter the length of the CSV file as an integer after calling the Python program.\n")

if __name__ == "__main__":
    main()
