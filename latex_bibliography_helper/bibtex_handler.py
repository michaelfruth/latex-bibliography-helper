import re

from bibtexparser.bwriter import BibTexWriter

import util


def hide_attribute(bib_entry):
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


def order_hidden_attributes(attributes: [str], order: [str]) -> None:
    """
    Inserts the hidden attributes into an existing attributes order. This function modifies 'order' as hidden attributes
    get inserted.

    Example:
        Hide prefix: "_"
        attributes = ["_author", "_booktitle", "title"]
        order = ["author", "title"]
    "_author" is considered as hidden attribute as it starts with the hide prefix. Actually, nothing will be ordered (
    and a random order will be selected by the BibTeX-Parser, because the names of the attributes do not match the names
    of the attributes to order. To get also an ordering of hidden attributes, these are inserted, based on their real
    attribute name, at the corresponding indices in the order list.
    The resulting order will be as follows: ["author", "_author", "title"]
    """

    hide_prefix = util.get_config_property("style", "hidePrefix")
    for attribute in attributes:
        if attribute.startswith(hide_prefix):
            plain_attribute = re.sub(f"^{hide_prefix}*", "", attribute)
            if plain_attribute in order:
                # Plain attribute exists in the attributes to order
                index = order.index(plain_attribute)  # Get index
                order.insert(index + 1, attribute)  # Insert hidden attribute into list containing the order


def get_attribute_names(only_hide=False) -> [str]:
    """
    Returns the names of all attributes. If 'only_hide' is set to true, only the attribute names for which the hide
    property is set to true will be returned.
    """

    # "attributes" : [
    #   "author",
    #   { "name": "author", "hide": True/False, ...}
    # ]
    attributes = util.get_config_property("style", "attributes")

    if only_hide:
        # Keep only hidden attributes
        attributes = [a for a in attributes if isinstance(a, dict) and a["hide"] is True]

    names = []
    for attribute in attributes:
        if isinstance(attribute, dict):
            names.append(attribute["name"])
        else:
            names.append(attribute)
    return names


def apply_bibtex_writer_style(writer: BibTexWriter) -> None:
    """
    Applies the common BibTeX style properties to the writer.
    """
    writer.indent = " " * 4
    writer.order_entries_by = None
    writer.align_values = True
