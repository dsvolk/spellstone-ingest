from datetime import datetime
from pprint import pprint

import feedparser


def parse_rss_feed(url, start_date):
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Convert the start_date to a datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # List to hold the filtered entries
    filtered_entries = []

    for entry in feed.entries:
        # Convert the entry's published date to a datetime object
        entry_date = datetime(*entry.published_parsed[:6])

        # Check if the entry date is after the start_date
        if entry_date >= start_date:
            filtered_entries.append(entry)

    return filtered_entries


# Example usage
rss_feed_url = "https://lexfridman.com/feed/podcast/"
start_date = "2024-01-01"
entries = parse_rss_feed(rss_feed_url, start_date)

pprint(entries)
