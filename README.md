## Tool to analyse the massive CSV file created by cactus-robot

---

### Requirements

- python 3.10
- click

### Recommended
- xsv

### Expected Input File

This program is designed to analyse and enrich a dataset curated by the program cactus-robot, which takes a list of URLs and uses tools from Sciences Po médialab (Minet, URAL) to enrich the URL data. Cactus robot produces the following data fields for each URL:

- **input** : the first URL seen by the program whose normalized version had not yet been cached
- **count** : the sum of all URLs in the dataset with the same normalized URL
- **normalized url** : the normalization of the input URL
- **domain** : the domain of the URL
- **subdomain** : the subdomain of the URL
- **complete subdomain** : the concatenation of the domain and subdomain
- **host name** : the host name extracted from the URL
- **normalized host name** : a normalized version of the host name
- **twitter user** : the handle of the Twitter user if URL is from a tweet
- **youtube channel name** : the name of the Youtube channel if the URL is from a video or channel
- **youtube channel id** : the id of the Youtube channel if the URL is from a video or channel
- **youtube channel link** : the link to the Youtube channel if the URL is from a video or channel
- **facebook group name** : the name of the Facebook group if the URL is from a Facebook group
- **facebook group id**: the id of the Facebook group if the URL is from a Facebook group

This program then analyses these data fields to produce agregations and summaries.

---
#### *Optional*

If you want to agregate multiple data files from a gazouilloire collection (ex. agregate data from consecutiv months into one file), the function `combine.py` can do this.

```python
python combine.py PATH/TO/DIRECTORY
```

The expected output is a file in the created directory `concatenated_data/` called  `agreg.csv`. It is recommended to manually modify the name of this file to better describe of what it is an agregation.

---

### Syntax

Call the function `main.py` with the positional arguments of (1) the file path to the CSV created by cactus-robot and (2) the length of this file. It is recommended to get this integer from the xsv command `xsv count`.

```
$ python main.py PATH/TO/MASSIVE-CSV-FILE.csv LENGTH-OF-MASSIVE-CSV
```
The expected output is a created directory called `enriched_data/` and the file `enriched_INPUT-CSV-FILE.csv` as well as four supplementary files: `sum_domain_INPUT-CSV-FILE.csv`, `sum_facebook_INPUT-CSV-FILE.csv`, `sum_twitter_INPUT-CSV-FILE.csv`, and `sum_youtube_INPUT-CSV-FILE.csv`.

### Method

In this early version, the program parses the CSV twice.

```python
def parse_csv(csv_file:str, length:str, outfile_name:str):

    # Count occurences
    reader = tqdm(generator(csv_file), total=int(length), desc="Counting Occurrences")
    [analyse_row(row, Counters) for row in reader]

    # Update results
    fieldnames = INPUT_FILE_FIELDNAMES+["domain count", "subdomain count", "youtube channel count", "facebook group count", "twitter account count"]
    with open(outfile_name, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        reader = tqdm(generator(csv_file), total=int(length), desc="Enriching Dataset")
        [enrich_row(row, Counters, writer) for row in reader]

    return Counters
```

1. On the first pass, the program counts the number of times a unique URL in the dataset satisfied certain research parameters. In particular, the preliminary parsing of the CSV file records if a unique url in the dataset is:

    - a link from a youtube channel [`youtube channel count`]

    - a link from a facebook group [`facebook group count`]

    - a link from a Twitter account [`twitter account count`]

    The function `analyse_row()` does not return anything, but rather updates variables which count the number of times a youtube channel, a facebook group, a twitter account, a domain [`domain count`], and a subdomain [`subdomain count`] appear in the dataset.

    The preliminary parsing also records the quantity of tweets that correspond to the researched data field. These sums are later reported in designated output files. For example, a file with the prefix "*sum_youtube_*" will present the following three details about the dataset:
    
    - [`youtube channel`] : the URL of every youtube channel
    - [`count of unique urls`] : the number of unique URLs from that channel that were present in the dataset
    - [`sum of tweets`] : the sum of all the tweets that contained links from that youtube channel

    Currently, the program will prepare 4 agregations: (1) domain names, (2) youtube channels, (3) facebook groups, (4) twitter accounts. The export of this agregations, however, is the last step of the program. It is not executed during the two passes through the input file.

2. Having collected data from the input file, the program then passes over the file a second time to "enrich" the CSV. At this point, data stored in variables created and informed during the first pass are used to rewrite (or "enrich") rows of the input file into a new output file.

    The output file is written iteratively over the course of the second pass through the input file in an effort to conserve memory. Because we are not exporting the data in a later step, there is no need for a variable that holds in the computer's memory all the data in the enriched dataset. This is desireable because the dataset is likely very large to begin with and will become larger with the enrichment.
