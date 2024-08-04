import re
import time
from datetime import datetime
from typing import List, Optional

import feedparser
import requests
from markdownify import markdownify
from prefect import task
from pydantic import BaseModel

# I probably need some way to persist the last date I checked the feed
# Maybe I can store it in a file or a database
# Makes sense to store it in a file in Obsidian vault, say in /.spellstone/feeds/lexfridman.yaml
# how do I retreive it if I run the script in the cloud, and only send the content to Obsidian via webhook?


def extract_date(dt: time) -> datetime:
    return datetime(*dt[:6]).date()


@task
def load_rss_feed(url: str, start_date: Optional[str] = None) -> List:
    # Parse the RSS feed
    feed = feedparser.parse(url)

    if start_date:
        # Convert the start_date to a datetime object
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_entries = []

        for entry in feed.entries:
            # Convert the entry's published date to a datetime object
            entry_date = datetime(*entry.published_parsed[:6])

            # Check if the entry date is after the start_date
            if entry_date >= start_date:
                filtered_entries.append(entry)
    else:
        filtered_entries = feed.entries

    # pprint(filtered_entries)
    return filtered_entries


class RSSFeedEntry(BaseModel):
    title: str
    summary: str
    link: str
    date_published: datetime


class PodcastEpisode(RSSFeedEntry):
    transcript: str | None = None


@task
def parse_rss_entry(entry) -> PodcastEpisode:
    # Extract the title, summary, and link
    title = entry.title
    summary = markdownify(entry.summary, escape_misc=False)
    link = entry.link

    # Extract the published date
    date_published = extract_date(entry.published_parsed)

    return PodcastEpisode(
        title=title,
        summary=summary,
        link=link,
        date_published=date_published,
    )


def url_to_markdown(url: str, ok_to_fail: bool = True) -> str:
    headers = {
        "Accept": "*/*",
    }
    response = requests.get(url, headers=headers)

    print(f"Fetching content from {url}...")
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")

    if response.status_code == 200:
        return markdownify(response.text, escape_misc=False)
    else:
        print(f"Failed to fetch the content from {url}. Status code: {response.status_code}")
        if ok_to_fail:
            return ""
        else:
            raise Exception(f"Failed to fetch the content from {url}. Status code: {response.status_code}")


@task
def parse_rss_entry_lex_friedman(entry) -> PodcastEpisode:
    # Extract the title, summary, and link
    feed_entry = parse_rss_entry(entry)

    # print(feed_entry.summary)

    transcript = None
    if transcript_url := re.search(r"Transcript:\s*(https?://[^\s]+)", feed_entry.summary):
        transcript = url_to_markdown(transcript_url.group(1))
    else:
        print("No transcript URL found in the feed entry summary.")

    return PodcastEpisode(
        title=feed_entry.title,
        summary=feed_entry.summary,
        link=feed_entry.link,
        date_published=feed_entry.date_published,
        transcript=transcript,
    )


@task
def parse_rss_entry_sean_carrols_mindscape(entry) -> PodcastEpisode:

    # Extract the title, summary, and link
    title = entry.title
    summary = markdownify(entry.description, escape_misc=False)
    print(summary)

    if blog_post_url_search := re.search(r"transcript:\s*<(https?://[^\s]+)>", summary):
        blog_post_url = blog_post_url_search.group(1)

        # Looks like this one is too difficult, yobany dynamic JS site which declines to be scraped

        # Attempt 1
        # blog_post = url_to_markdown(blog_post_url)

        # Attempt 2
        # blog_post = trafilatura.extract(
        #     blog_post_url, output_format="txt", include_tables=True, include_comments=True, deduplicate=True
        # )

    else:
        print("No blog post URL found in the feed entry description.")
        blog_post_url = ""

    # Extract the published date
    date_published = extract_date(entry.published_parsed)

    return PodcastEpisode(
        title=title,
        summary=summary,
        link=blog_post_url,
        date_published=date_published,
        transcript=None,
    )
