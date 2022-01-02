from bibtexparser.bwriter import BibTexWriter
import logging
from handler import bibtex_handler

import bibtexparser

import util
import config

logger = logging.getLogger(__name__)


def style(bib_database, curlify, pretty):
    all_attributes = set()

    for bib_entry in bib_database.entries:
        if curlify:
            util.curlify_title(bib_entry)
        if pretty:
            util.hide_attributes(bib_entry)
            if config.is_rewrite_booktitle():
                util.rewrite_booktitle(bib_entry)

        util.hide_attributes(bib_entry)

        # Collect all attributes
        all_attributes.update(list(bib_entry.keys()))

    writer = BibTexWriter()

    attributes_order = writer.display_order
    if config.is_sort_attributes():
        # Order attributes
        attributes_order = bibtex_handler.create_attributes_order(all_attributes,
                                                                  config.get_attribute_names(),
                                                                  config.get_hide_prefix())
    writer.display_order = attributes_order

    bib = writer.write(bib_database)
    return bib


def beautify(content, curlify, copy_to_clipboard, pretty):
    parser = bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False,
                                               common_strings=True)
    bib_database = bibtexparser.loads(content, parser=parser)

    content = style(bib_database, curlify, pretty)

    if copy_to_clipboard:
        util.copy_to_clipboard(content)
    print(content)
