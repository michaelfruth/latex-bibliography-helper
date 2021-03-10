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


def parse(file):
    with open(file, "r") as bib_file:
        return bibtexparser.load(bib_file, parser=bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False))


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
    writer.indent = " " * 2
    writer.order_entries_by = None
    writer.align_values = True

    # Preserve order of BIB-Items from DBLP
    writer.display_order = bib_util.get_bib_order()

    bib = writer.write(bib_database)

    bib_util.copy_to_clipboard(bib)

    print(bib)
    print("Copied to clipboard!")


def main(file, curly_title):
    bib_database = parse(file)
    pretty(bib_database, curly_title)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("file", help="The file to pretty print", nargs="+")
    parser.add_argument("-c", help="Set another pair of curly brackets around the tile", action="store_true")
    args = parser.parse_args()

    file = " ".join(args.file)
    if not path.isfile(file):
        print("'{}' could not be found!".format(file))
        exit(1)
    main(file, args.c)
