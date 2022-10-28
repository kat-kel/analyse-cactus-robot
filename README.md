## Tool to analyse the massive CSV file created by cactus-robot

---

### Requirements

- python 3.10
- click

### Recommended
- xsv

### Syntax

Call the function `main.py` with the positional arguments of (1) the file path to the CSV created by cactus-robot, 
(2) the length of this file. It is recommended to get this integer from the xsv command `xsv count`.

```
$ python main.py PATH/TO/MASSIVE-CSV-FILE.csv LENGTH-OF-MASSIVE-CSV
```
The expected output is a file in the same directory as this application called `enriched_MASSIVE-CSV-FILE.csv`

### Method

The method could be improved. Currently, it parses the CSV twice. On the first pass (`parse_rows.count_fields()`), 
the program counts the number of times a unique URL in the dataset had: 

- a certain domain [`domain count`]

- a certain subdomain [`subdomain count`]

- a link from a certain youtube channel [`youtube channel count`]

- a link from a certain facebook group [`facebook group count`]

- a link from a certain Twitter account [`twitter account count`]

This data is then added to the original dataset, rather than being exported in its own format (though it exists in `Counter` objects--and can be easily printed).
The data is added by reading the CSV for a second time and *enriching* the row (`parse_rows.enrich_row()`) by updating that unique URL's metadata with the 
number of times its (a) domain, (b) subdomain, (c) youtube channel, (d) facebook group, and/or (e) Twitter account appear among the set of unique URLs.
 
 ## What's still missing
 
 What's missing is the relationship between the number of times a URL's domain appears in the dataset and the number of time that URL was in the original data.
 
|input|count|normalized ur|domain|...|youtube channel link|...|domain count|youtube channel count|facebook group count|twitter account count|
|---|---|---|---|---|---|---|---|---|---|---|
|https:// youtube.com /video|3|youtube.com/video|youtube.com|...|youtube.com/video|...|128096|73|  |  |

In the enriched dataset, every unique URL has a `count` meaning the number of times that URL appeared in the original data, and now it has the enriched 
count of how many times certain elements of its metadata were present in the dataset. It lacks a meaningful relationship between these two data.
