import logging

import bibtexparser
from bibhelper.config import is_sort_attributes, is_rewrite_booktitle
from bibhelper.handler.bibtex_handler import apply_bibtex_writer_style, create_attributes_order
from bibhelper.util import curlify_title, rewrite_booktitle, get_attribute_names, hide_attributes, get_hide_prefix, \
    copy_to_clipboard
from bibtexparser.bwriter import BibTexWriter

logger = logging.getLogger(__name__)


def style(bib_database, curlify, pretty):
    all_attributes = set()

    for bib_entry in bib_database.entries:
        if curlify:
            curlify_title(bib_entry)
        if pretty:
            hide_attributes(bib_entry)
            if is_rewrite_booktitle():
                rewrite_booktitle(bib_entry)

        # Collect all attributes
        all_attributes.update(list(bib_entry.keys()))

    writer = BibTexWriter()
    apply_bibtex_writer_style(writer)

    attributes_order = writer.display_order
    if is_sort_attributes():
        # Order attributes
        attributes_order = create_attributes_order(all_attributes,
                                                   get_attribute_names(),
                                                   get_hide_prefix())
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
