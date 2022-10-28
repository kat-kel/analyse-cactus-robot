from fieldnames import ADDITIONAL_OUTPUT_FIELDNAMES


def count_fields(row, counters):

    domain = row.get("domain")
    subdomain = row.get("subdomain") # change to "complete subdomain"
    youtube_channel = row.get("youtube channel link")
    facebook_group = row.get("facebook group name") or row.get("facebook group id")
    twitter_user = row.get("twitter user")

    update_counter(counters.domain, domain)
    update_counter(counters.subdomain, subdomain)
    update_counter(counters.youtube_channel, youtube_channel)
    update_counter(counters.facebook_group, facebook_group)
    update_counter(counters.twitter_user, twitter_user)


def update_counter(counter,value):
    if value:
        counter.update([value])


def enrich_row(row, counters):

    row_domain = row.get("domain")
    row_subdomain = row.get("subdomain") # change to "complete subdomain"
    row_youtube_channel_link = row.get("youtube channel link")
    row_facebook_group = row.get("facebook group name") or row.get("facebook group id")
    row_twitter_user = row.get("twitter user")

    # number of times a url had this domain
    if row_domain and row_domain in counters.domain.keys():
        row.update({ADDITIONAL_OUTPUT_FIELDNAMES[0]:counters.domain[row_domain]})

    # number of times a url had this subdomain
    if row_subdomain and row_subdomain in counters.subdomain.keys():
        row.update({ADDITIONAL_OUTPUT_FIELDNAMES[1]:counters.subdomain[row_subdomain]})

    # number of times a url was from this youtube channel
    if row_youtube_channel_link and row_youtube_channel_link in counters.youtube_channel.keys():
        row.update({ADDITIONAL_OUTPUT_FIELDNAMES[2]:counters.youtube_channel[row_youtube_channel_link]})

    # number of times a url was from this facebook group
    if row_facebook_group and row_facebook_group in counters.facebook_group.keys():
        row.update({ADDITIONAL_OUTPUT_FIELDNAMES[3]:counters.facebook_group[row_facebook_group]})

    # number of times a url was from this twitter account
    if row_twitter_user and row_twitter_user in counters.twitter_user.keys():
        row.update({ADDITIONAL_OUTPUT_FIELDNAMES[4]:counters.twitter_user[row_twitter_user]})

    return row
