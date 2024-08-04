from typing import Callable

from prefect import flow

from ..markdown.md import make_markdown, sanitize_filename
from ..obsidian_webhooks.post import post_to_webhook
from ..rss.rss import (
    load_rss_feed,
    parse_rss_entry,
    parse_rss_entry_lex_friedman,
    parse_rss_entry_sean_carrols_mindscape,
)

# from pprint import pprint


@flow
def pull_rss_feed(feed_name: str, feed_url: str, vault_dir: str, parse_fn: Callable, start_date: str = None):

    entries = load_rss_feed(feed_url, start_date)

    for raw_entry in entries:
        entry = parse_fn(raw_entry)

        body = f"""# {entry.title}
by {feed_name}
## Summary
{entry.summary}

## Transcript
{entry.transcript if entry.transcript else "No transcript available."}
"""

        md = make_markdown(
            frontmatter={
                "created": entry.date_published,
                "modified": entry.date_published,
                "tags": ["ingest", "rss", "talk"],
                "url": entry.link,
            },
            body=body,
        )

        # pprint(md)

        post_to_webhook(
            file_path=f"{vault_dir}/{sanitize_filename(entry.title)}.md",
            markdown_content=md,
        )


if __name__ == "__main__":

    pull_rss_feed(
        feed_name="[[@Lex Fridman|Lex Fridman (Podcast)]]",
        feed_url="https://lexfridman.com/feed/podcast/",
        vault_dir="ingest/rss",
        parse_fn=parse_rss_entry_lex_friedman,
        start_date="2024-04-01",
    )

    pull_rss_feed(
        feed_name="[[Cognitive Revolution (podcast)]]",
        feed_url="https://feeds.megaphone.fm/RINTP3108857801",
        vault_dir="ingest/rss",
        parse_fn=parse_rss_entry,
        start_date="2024-04-01",
    )

    pull_rss_feed(
        feed_name="[[Mindscape (podcast)]]",
        feed_url="https://rss.art19.com/sean-carrolls-mindscape",
        vault_dir="ingest/rss",
        parse_fn=parse_rss_entry_sean_carrols_mindscape,
        start_date=None,
    )

    pull_rss_feed(
        feed_name="[[Истории кино (podcast)]]",
        feed_url="https://cloud.mave.digital/55799",
        vault_dir="ingest/rss",
        parse_fn=parse_rss_entry,
        start_date=None,
    )
