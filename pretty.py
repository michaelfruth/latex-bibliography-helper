import re
import bib_util

import logging
import subprocess
from os import path

import bibtexparser
from bibtexparser.bwriter import BibTexWriter

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

curly_title_pattern = re.compile('^{.*}$', re.DOTALL)


def pretty(bib_database, curly_title):
    if curly_title:
        for entry in bib_database.entries:
            if "title" in entry:
                title = entry['title']

                # Check if curly brackets are already set
                if not re.fullmatch(curly_title_pattern, title):
                    entry['title'] = "{{{}}}".format(entry['title'])

    # Apply BIB-Item style
    writer = BibTexWriter()
    writer.indent = " " * 4
    writer.order_entries_by = None
    writer.align_values = True

    # Preserve order of BIB-Items from DBLP
    writer.display_order = bib_util.get_bib_order()

    bib = writer.write(bib_database)

    bib_util.copy_to_clipboard(bib)

    print(bib)
    print("Copied to clipboard!")


def main(content, curly_title):
    bib_database = bibtexparser.loads(content, parser=bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False))
    pretty(bib_database, curly_title)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    input = parser.add_mutually_exclusive_group(required=True)
    input.add_argument("-f", help="The file to pretty print")
    input.add_argument("-cb", help="Use the clipboard", action="store_true")

    parser.add_argument("-c", help="Set another pair of curly brackets around the tile", action="store_true")
    args = parser.parse_args()

    if args.f:
        # File was specified
        if not path.isfile(args.f):
            print("'{}' could not be found!".format(args.f))
            exit(1)
        else:
            with open(args.f, "r") as f:
                content = f.read()
            main(content, args.c)

    if args.cb:
        # Use clipboard
        main(bib_util.copy_from_clipboard(), args.c)
