from collections import Counter, namedtuple
import csv

from tqdm.auto import tqdm

from fieldnames import INPUT_FILE_FIELDNAMES

Counters = namedtuple("Counters", ["domain", "subdomain", "youtube_channel", "facebook_group", "twitter_user", "sum_domains", "sum_facebook", "sum_youtube", "sum_twitter"])
Counters.domain = Counter({})
Counters.subdomain = Counter({})
Counters.youtube_channel = Counter({})
Counters.facebook_group = Counter({})
Counters.twitter_user = Counter({})

Counters.sum_domains = {}
Counters.sum_facebook = {}
Counters.sum_youtube = {}
Counters.sum_twitter = {}


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


def analyse_row(row, counters):

    # Extract data from the row
    count = row.get("count")
    domain, subdomain, youtube_channel, facebook_group, twitter_user = get_row_data(row)

    fields_for_count_of_unique_url = [("domain", domain), ("subdomain", subdomain), ("youtube_channel", youtube_channel), ("facebook_group", facebook_group), ("twitter_user", twitter_user)]
    # Update the counter of unique URLs for each desired field
    [update_counter(getattr(counters, field[0]), field[1]) for field in fields_for_count_of_unique_url]

    # Update the running sum of tweets for each desired field
    fields_for_sum_of_all_tweets = [("sum_domains", domain), ("sum_facebook", facebook_group), ("sum_youtube", youtube_channel), ("sum_twitter", twitter_user)]
    [update_sum(getattr(counters, field[0]), field[1], count) for field in fields_for_sum_of_all_tweets]


def enrich_row(row, counters, writer):

    domain, subdomain, youtube_channel, facebook_group, twitter_user = get_row_data(row)

    EnrichedData = namedtuple("EnrichedData", ["value", "counter", "header"])
    encriched_fields = [EnrichedData(domain, counters.domain, "domain count"), EnrichedData(subdomain, counters.subdomain, "subdomain count"), EnrichedData(youtube_channel, counters.youtube_channel, "youtube channel count"), EnrichedData(facebook_group, counters.facebook_group, "facebook group count"), EnrichedData(twitter_user, counters.twitter_user, "twitter account count")]

    [row.update({field.header: field.counter.get(field.value)}) 
    for field in encriched_fields 
    if field.value and field.value in field.counter.keys()]

    writer.writerow(row)


def generator(filepath:str):
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        yield from reader


def update_sum(counter, domain, count):
    old_sum = counter.get(domain)
    if old_sum:
        new_count = int(old_sum) + int(count)
    else:
        new_count = int(count)
    counter.update({domain:new_count})


def update_counter(counter_url, value):
    if value:
        counter_url.update([value])


def get_row_data(row):
    domain = row.get("domain")
    subdomain = row.get("complete subdomain")
    youtube_channel = row.get("youtube channel link")
    facebook_group = row.get("facebook group name") or row.get("facebook group id")
    twitter_user = row.get("twitter user")
    return domain, subdomain, youtube_channel, facebook_group, twitter_user
