import os
import urllib.parse

import requests
from dotenv import load_dotenv
from prefect import task

load_dotenv(override=True, verbose=True)


OBSIDIAN_WEBHOOK_URL = os.environ.get("OBSIDIAN_WEBHOOK_URL")


def encode_string_for_url(input_string: str) -> str:
    encoded_string = urllib.parse.quote(input_string)
    return encoded_string


@task
def post_to_webhook(file_path: str, markdown_content: str) -> None:
    """
    Posts markdown content to a webhook.

    :param webhook_url: The base URL of the webhook.
    :param file_path: The path of the file to update (used as a query parameter).
    :param markdown_content: The markdown content to insert into the file.
    """

    full_url = f"{OBSIDIAN_WEBHOOK_URL}?path={encode_string_for_url(file_path)}"
    headers = {"Content-Type": "text/markdown"}
    response = requests.post(full_url, headers=headers, data=markdown_content.encode("utf-8"), timeout=10)

    # Check for successful response
    if response.status_code == 200:
        print("Successfully posted to the webhook.")
    else:
        print(f"Failed to post to the webhook. Status code: {response.status_code}, response: {response.text}")
        raise Exception(
            f"Failed to send the message to the Obsidian webhook: [{response.status_code}] {response.text}"
        )
