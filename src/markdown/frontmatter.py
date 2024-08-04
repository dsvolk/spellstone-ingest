import yaml


def parse_frontmatter(frontmatter: str) -> dict:
    """
    Parses the frontmatter string into a dictionary.

    Args:
    - frontmatter (str): The frontmatter string to parse.

    Returns:
    - dict: A dictionary with keys and values or lists of values.
    """
    try:
        # Use yaml.safe_load to parse the frontmatter
        parsed_data = yaml.safe_load(frontmatter)
        return parsed_data
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")
        return {}


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def represent_none(self, _):
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


def compose_frontmatter(data: dict) -> str:
    """
    Composes a frontmatter string from a dictionary.

    Args:
    - data (dict): A dictionary with keys and values or lists of values.

    Returns:
    - str: The frontmatter string.
    """
    try:
        # Use yaml.dump to compose the frontmatter
        frontmatter = yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            explicit_start=False,
            explicit_end=False,
            Dumper=IndentDumper,
            allow_unicode=True,
        )
        return frontmatter
    except yaml.YAMLError as exc:
        print(f"Error composing YAML: {exc}")
        return ""
