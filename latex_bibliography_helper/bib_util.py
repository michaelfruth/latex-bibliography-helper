import re
from typing import Union

import pyperclip
from bibtexparser.bwriter import BibTexWriter

_config = None
_default_config = {
    "settings": {
        "search": {
            "publicationUrl": "http://dblp.org/search/publ/api?q={}&format=json",
            "authorUrl": "http://dblp.org/search/author/api?q={}&format=json",
            "venueUrl": "http://dblp.org/search/venue/api?q={}&format=json"
        }
    },
    "style": {
        "hidePrefix": "_",
        "sort": True,
        "attributes": []
    }
}


def get_config_property(*args):
    current_element = _config

    for arg in args:
        if not isinstance(current_element, dict):
            raise TypeError("Trying to access a non-dictionary configuration element by key: '{}'.\n"
                            "Element: {}".format(arg, current_element))
        if arg not in current_element:
            raise ValueError("Could not find/access attribute '{}' in configuration.\n"
                             "Current element: '{}'".format(arg, current_element))

        current_element = current_element[arg]

    return current_element


def set_config_or_default(config=None):
    global _config
    _config = config if config is not None else _default_config


def extract_booktitle_shortname(booktitle: str) -> Union[str, None]:
    """
    Tries to extract the shortname of the booktitle of a publication. Curly brackets around the title are ignored and
    won't be returned either.

    The following patterns will be recognized.:
    - Shortname followed by year: ... {SHORTNAME} YEAR ....
    - Example: 43rd {ACM/IEEE} Annual ..., {ISCA} 2016, Seoul, South Korea, June 18-22, 2016

    - Shortname at the end: ... {SHORTNAME}
    - Example: 2014 IEEE International Symposium on Workload Characterization {IISWC}

    - Shortname at the beginning: {SHORTNAME} 'YEAR...
    - Example: {PACT} '20: International Conference on Parallel Architectures and Compilation Techniques

    Returns the extracted shortname if found, None otherwise.
    """
    patterns = []

    shortname_year_pattern = re.compile(r'{?\w+}?(?=(\n|\r|\s)+[0-9]{4})')
    patterns.append(shortname_year_pattern)

    shortname_end_pattern = re.compile(r'{[^{]*}$')
    patterns.append(shortname_end_pattern)

    shortname_start_pattern = re.compile(r'(^{?.*}?)(?:(\n|\r|\s)+\'[0-9]{2,4})')
    patterns.append(shortname_start_pattern)

    for shortname_pattern in patterns:
        findings = re.search(shortname_pattern, booktitle)
        if findings:
            # TODO: What if multiple groups were found?
            shortname_groups = findings.groups()

            if len(shortname_groups) >= 1 and len(shortname_groups[0].strip()) > 0:
                # Use groups() for non-capturing groups
                shortname = shortname_groups[0]
            else:
                shortname = findings.group(0)

            # Remove curly braces
            if shortname.startswith("{"):
                shortname = shortname[1:]
            if shortname.endswith("}"):
                shortname = shortname[:-1]
            return shortname
    return None


def curlify_title(title: str) -> str:
    """
    Adds a pair of curly braces to the title. If the title already contains curly brackets, nothing will happen.

    Example:
    - curlify_title("Hello") returns "{Hello}".
    - curlify_title("{Hello}") returns "{Hello}".
    """
    curly_title_pattern = re.compile(r'^{.*}$', re.DOTALL)
    # Check if curly brackets are already set
    if not re.fullmatch(curly_title_pattern, title):
        # Add extra curly brackets to title. Preserves lowercase/uppercase in BIBTeX
        title = "{{{}}}".format(title)
    return title


def hide_attributes(bib_entry):
    attributes_to_hide = get_attribute_names_to_hide()

    hide_prefix = get_config_property("style", "hidePrefix")
    for original_attribute in attributes_to_hide:
        if original_attribute not in bib_entry:
            # Nothing to hide if attribute is not contained in the BIBTeX
            continue

        hidden_attribute = hide_prefix + original_attribute
        while hidden_attribute in bib_entry:
            # The attribute exists twice, once as visible and once as hidden.
            # We don't want to override/delete any element.
            # Add more prefixes until a non-existing hidden attribute name is found.
            hidden_attribute = hide_prefix + hidden_attribute

        bib_entry[hidden_attribute] = bib_entry[original_attribute]
        del bib_entry[original_attribute]


def order_hidden_attributes(attributes: [str], attributes_order: [str]) -> None:
    hide_prefix = get_config_property("style", "hidePrefix")
    print(attributes_order)
    for attribute in attributes:
        if attribute.startswith(hide_prefix):
            plain_attribute = re.sub(f"^{hide_prefix}*", "", attribute)
            if plain_attribute in attributes_order:
                index = attributes_order.index(plain_attribute)  # Get index
                attributes_order.insert(index + 1, attribute)  # Insert hidden attribute into list containing the order
    print(attributes_order)


def get_attribute_names_to_hide():
    attributes = get_config_property("style", "attributes")

    # "attributes": [
    #   {"name": ..., "hide": true/false},
    #   ...
    # ]

    hide = []
    for attribute in attributes:
        if isinstance(attribute, dict):
            if attribute["hide"]:
                hide.append(attribute["name"])

    return hide


def get_attributes_order():
    attributes = get_config_property("style", "attributes")

    # "attributes" : [
    #   "author",
    #   { "name": "author", ...}
    # ]

    order = []
    for attribute in attributes:
        if isinstance(attribute, dict):
            order.append(attribute["name"])
        else:
            order.append(attribute)

    return order


def get_bibtex_writer() -> BibTexWriter:
    writer = BibTexWriter()
    # Apply BIB-Item style
    writer.indent = " " * 4
    writer.order_entries_by = None
    writer.align_values = True
    return writer


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def read_from_clipboard() -> str:
    return pyperclip.paste()
