import re

from bibtexparser.bwriter import BibTexWriter


def create_attributes_order(current_attributes: [str], plain_attributes_order: [str], hide_prefix: str) -> [str]:
    """
    Creates an order of the current attributes based on the plain attributes considering the hide prefix.

    Example:
        hide_prefix: "_"
        current_attributes = ["author", "booktitle", "title", "_author"]
        plain_attributes_order = ["booktitle", "author"]

    Result will be:
        ["booktitle", "author", "_author", "title"]

    Hidden attributes will be considered for the order.
    """

    final_order = [*plain_attributes_order]
    for current_attribute in current_attributes:
        if current_attribute.startswith(hide_prefix):
            plain_attribute = re.sub(f"^{hide_prefix}*", "", current_attribute)
            if plain_attribute in plain_attributes_order:
                # Plain attribute exists in the attributes to order.
                # Get Index and Insert hidden attribute into list containing the order
                index = final_order.index(plain_attribute)
                final_order.insert(index + 1, current_attribute)
    return final_order


def hide_attributes(bib_entry: dict, attributes_to_hide: [str], hide_prefix: str) -> None:
    """
    The attributes to hide are replaced by adding a prefix (hide_prefix).
    Existing attributes are *not* overwritten, meaning the hide prefix will be concatenated as long as a non-existing
    hidden attribute name is found. E.g.:

    Existing attributes of the bibtex entry:
    author
    _author
    __author

    After processing (hide_prefix set to "_"):
    _author
    __author
    ___author (previous "author" attribute)
    """
    for attribute_name in attributes_to_hide:
        if attribute_name not in bib_entry:
            # Attribute does not exist. Skip it..
            continue

        # Attribute exists in bib_entry. Hide it (by replacing the name of the attribute with hide_prefix + name)!
        hidden_attribute_name = hide_prefix + attribute_name
        while hidden_attribute_name in bib_entry:
            # The attribute exists twice, once as visible and once as hidden.
            # We don't want to override/delete any element.
            # Add more prefixes until a non-existing hidden attribute name is found.
            hidden_attribute_name = hide_prefix + attribute_name

        # Add attribute as hidden attribute
        bib_entry[hidden_attribute_name] = bib_entry[attribute_name]
        # Delete original "visible" attribute (without the prefix)
        del bib_entry[attribute_name]


def apply_bibtex_writer_style(writer: BibTexWriter) -> None:
    """
    Applies the common BibTeX style properties to the writer.
    """
    writer.indent = " " * 4
    writer.order_entries_by = None
    writer.align_values = True
