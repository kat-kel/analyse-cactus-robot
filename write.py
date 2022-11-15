import csv
import os
from collections import Counter, namedtuple


Summary = namedtuple("Summary", ["outfile_prefix", "column_header", "count_of_urls", "sum_of_tweets"])
domain = Summary("sum_domains_", "domain", "domain", "sum_domains")
facebook = Summary("sum_facebook_", "facebook group", "facebook_group", "sum_facebook")
youtube = Summary("sum_youtube_", "youtube channel", "youtube_channel", "sum_youtube")
twitter = Summary("sum_twitter_", "twitter account", "twitter_user", "sum_twitter")


def write_summary(counters, out_directory, basename):
    [summary(subject.column_header, # header for first column in outfile
    getattr(counters, subject.count_of_urls), # count of unique urls for this subject
    getattr(counters, subject.sum_of_tweets), # count of all tweets for this subject 
    os.path.join(out_directory, f"{subject.outfile_prefix}{basename}")) # name of outfile
    for subject in [domain,facebook,youtube,twitter]]


def summary(subject, count_of_urls:Counter, sum_of_tweets:dict, outfile_name):
    print(f"Writing Summary of {subject}")
    with open(outfile_name, "w") as f:
        writer = csv.DictWriter(f, fieldnames=[subject, "count of unique urls", "sum of tweets"])
        writer.writeheader()
        [writer.writerow(
            {subject:value, "count of unique urls":count, "sum of tweets":sum_of_tweets[value]}) 
        for value,count in count_of_urls.most_common() 
        if sum_of_tweets.get(value)]
