import logging

from bibhelper import config
from bibhelper import handler_util
from bibhelper.handler import bibtex_handler
from bibhelper.util import copy_to_clipboard

logger = logging.getLogger(__name__)


def style(bib_database, curlify, pretty):
    all_attributes = set()

    for bib_entry in bib_database.entries:
        if curlify:
            handler_util.curlify_title(bib_entry)
        if pretty:
            handler_util.hide_attributes(bib_entry)
            if config.is_rewrite_booktitle():
                handler_util.rewrite_booktitle(bib_entry)

        # Collect all attributes
        all_attributes.update(list(bib_entry.keys()))

    writer = bibtex_handler.get_bibtex_writer()

    attributes_order = writer.display_order
    if config.is_sort_attributes():
        # Order attributes
        attributes_order = bibtex_handler.create_attributes_order(all_attributes,
                                                                  config.get_attribute_names(),
                                                                  config.get_hide_prefix())
    writer.display_order = attributes_order

    bib = writer.write(bib_database)
    return bib


def beautify(content, curlify, is_copy_to_clipboard, pretty):
    bib_database = bibtex_handler.load_bibtex_database(content)

    content = style(bib_database, curlify, pretty)

    if is_copy_to_clipboard:
        copy_to_clipboard(content)
    print(content)
