import logging

import bibtexparser
from bibhelper import config
from bibhelper import handler_util
from bibhelper.handler import bibtex_handler
from bibhelper.util import copy_to_clipboard
from bibtexparser.bwriter import BibTexWriter

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

    writer = BibTexWriter()
    bibtex_handler.apply_bibtex_writer_style(writer)

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
    parser = bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False,
                                               common_strings=True)
    bib_database = bibtexparser.loads(content, parser=parser)

    content = style(bib_database, curlify, pretty)

    if is_copy_to_clipboard:
        copy_to_clipboard(content)
    print(content)
