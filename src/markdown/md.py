import re

from .frontmatter import compose_frontmatter


def sanitize_filename(title: str) -> str:
    # Define a regex pattern for invalid filename characters
    invalid_chars = r'[\/:*?"<>|#]'

    # Replace invalid characters with an underscore
    sanitized_title = re.sub(invalid_chars, "_", title)

    # Strip leading and trailing whitespaces
    sanitized_title = sanitized_title.strip()

    # Optionally, truncate the filename to a maximum length (e.g., 255 characters for many filesystems)
    max_length = 255
    sanitized_title = sanitized_title[:max_length]

    return sanitized_title


def make_markdown(frontmatter, body):
    """
    Create a markdown multi-line string with frontmatter and body.

    :param frontmatter: Dictionary containing frontmatter keys and values.
    :param body: String containing the body of the markdown.
    :return: String containing the complete markdown content.
    """

    # Convert the frontmatter dictionary to a YAML string
    frontmatter_yaml = compose_frontmatter(frontmatter)

    # Combine the frontmatter and body into a markdown string
    markdown = f"---\n{frontmatter_yaml}\n---\n{body}"

    return markdown
