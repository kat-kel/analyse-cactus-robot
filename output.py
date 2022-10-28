import csv

from fieldnames import ADDITIONAL_OUTPUT_FIELDNAMES, INPUT_FILE_FIELDNAMES


def writer(results:dict, title:str):
    fieldnames = INPUT_FILE_FIELDNAMES+ADDITIONAL_OUTPUT_FIELDNAMES
    with open(title, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
