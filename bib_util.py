import re

import pyperclip
from bibtexparser.bwriter import BibTexWriter

_config = None


def get_config(*args):
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


def set_config(config):
    global _config
    _config = config


def curlify_title(bib_entry):
    curly_title_pattern = re.compile('^{.*}$', re.DOTALL)
    if "title" in bib_entry:
        title = bib_entry['title']

        # Check if curly brackets are already set
        if not re.fullmatch(curly_title_pattern, title):
            # Add extra curly brackets to title. Preserves lowercase/uppercase in BIBTeX
            bib_entry['title'] = "{{{}}}".format(title)


def hide_attributes(bib_entry):
    attributes_to_hide = get_attribute_names_to_hide()

    hide_prefix = get_config("style", "hidePrefix")
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
    hide_prefix = get_config("style", "hidePrefix")

    for attribute in attributes:
        if attribute.startswith(hide_prefix):
            plain_attribute = re.sub(f"^{hide_prefix}*", "", attribute)
            if plain_attribute in attributes_order:
                index = attributes_order.index(plain_attribute)  # Get index
                attributes_order.insert(index + 1, attribute)  # Insert hidden attribute into list containing the order


def get_attribute_names_to_hide():
    attributes = get_config("style", "attributes")

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
    attributes = get_config("style", "attributes")

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
