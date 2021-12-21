import re
from typing import Union

import pyperclip
from bibtexparser.bwriter import BibTexWriter


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
