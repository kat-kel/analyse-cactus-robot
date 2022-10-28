from collections import Counter, namedtuple

from tqdm.auto import tqdm

from fieldnames import COUNTER_FIELDNAMES
from generator import generator
from parse_row import count_fields, enrich_row


def parse_csv(csv, count):

    int(count)

    # Count occurences
    reader = tqdm(generator(csv), total=int(count), desc="Counting Occurrences")

    Counters = namedtuple("Counters", COUNTER_FIELDNAMES)
    Counters.domain = Counter({})
    Counters.subdomain = Counter({})
    Counters.youtube_channel = Counter({})
    Counters.facebook_group = Counter({})
    Counters.twitter_user = Counter({})

    [count_fields(row, Counters) for row in reader]

    # Update results
    reader = tqdm(generator(csv), total=int(count), desc="Updating Results")
    return [enrich_row(row, Counters) for row in reader], Counters
