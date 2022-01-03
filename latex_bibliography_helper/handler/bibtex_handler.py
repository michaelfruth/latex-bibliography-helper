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
    existing_attributes_to_order = {}
    for current_attribute in current_attributes:
        plain_attribute = re.sub(f"^{hide_prefix}*", "", current_attribute)
        if plain_attribute in plain_attributes_order:
            # Plain attribute exists in the attributes to order.
            # Get Index and Insert hidden attribute into list containing the order
            if plain_attribute not in existing_attributes_to_order:
                existing_attributes_to_order[plain_attribute] = []
            existing_attributes_to_order[plain_attribute].append(current_attribute)

    final_order = []
    for plain_attribute_order in plain_attributes_order:
        if plain_attribute_order in existing_attributes_to_order:
            existing_attributes = existing_attributes_to_order[plain_attribute_order]
            # Sort and reverse, otherwise hide prefix might be before the plain attribute name
            existing_attributes = reversed(sorted(existing_attributes))
            final_order.extend(existing_attributes)

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
            hidden_attribute_name = hide_prefix + hidden_attribute_name

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
    writer.align_multiline_values = False
