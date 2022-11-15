import os

import click

from parseCSV import parse_csv
from write import write_results, write_summary


@click.command
@click.argument("csv")
@click.argument("count")
def main(csv, count):

    out_directory = "enriched_data"

    if not os.path.isdir(out_directory):
        os.mkdir(out_directory)

    if os.path.isfile(csv):

        basename = os.path.basename(csv)

        outfile_name = os.path.join(out_directory, f"enriched_{basename}")

        try:
            # Test that the count parameter can be cast as an integer
            int(count)

            # Analyse data
            counters = parse_csv(csv,count, outfile_name)

            # Output results
            #write_results(results, title)
            write_summary(counters, out_directory, basename)

        except ValueError as err:
            print(f"\n{err}\n\
                Please enter the length of the CSV file as an integer.\n")


if __name__ == "__main__":
    main()
