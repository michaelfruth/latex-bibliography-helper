import logging

import bibtexparser

import bib_util

logger = logging.getLogger(__name__)


def style(bib_database, curlify):
    all_attributes = set()

    for bib_entry in bib_database.entries:
        if curlify:
            bib_util.curlify_title(bib_entry)

        bib_util.hide_attributes(bib_entry)

        # Collect all attributes
        all_attributes.update(list(bib_entry.keys()))

    writer = bib_util.get_bibtex_writer()

    if bib_util.get_config("style", "sort"):
        attributes_order = bib_util.get_attributes_order()
        bib_util.order_hidden_attributes(all_attributes, attributes_order)

        writer.display_order = attributes_order

    bib = writer.write(bib_database)
    return bib


def beautify(content, curlify, copy_to_clipboard):
    parser = bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False,
                                               common_strings=True)
    bib_database = bibtexparser.loads(content, parser=parser)

    content = style(bib_database, curlify)

    if copy_to_clipboard:
        bib_util.copy_to_clipboard(content)
    print(content)
