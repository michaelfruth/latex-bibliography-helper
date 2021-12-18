import json
import logging

import bibtexparser
import requests
from bibtexparser.bwriter import BibTexWriter

import bib_util

logger = logging.getLogger(__name__)


class Publication:

    def __init__(self, hit):
        info = hit["info"]
        self.url = info["url"]
        self.key = info["key"]

        self.ee = info.get("ee")
        self.doi = info.get("doi")

        authors = info["authors"]["author"]
        if not isinstance(authors, list):
            authors = [authors]
        self.authors = [Author(author) for author in authors]

        self.title = info["title"]
        self.venue = info.get("venue")
        self.volume = info.get("volume")
        self.number = info.get("number")
        self.pages = info.get("pages")
        self.chapter = info.get("chapter")
        self.isbn = info.get("isbn")
        self.publisher = info.get("publisher")
        self.series = info.get("series")
        self.year = info.get("year")
        self.type = info.get("type")
        self.sub_type = info.get("sub_type")
        self.isbn = info.get("isbn")

    def __str__(self):
        return "Title: {}\nAuthors: {}\n{} ({})".format(self.title,
                                                        ", ".join([str(author) for author in self.authors]),
                                                        self.venue,
                                                        self.year)


class Author():
    def __init__(self, author):
        self.pid = author["@pid"]
        self.name = author["text"]

    def __str__(self):
        return self.name


def load_publications(url):
    logger.info("Fetching publication from: {}".format(url))

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Fetching publications was not successful. Website returned error code '{}'.\n"
                         "URL: ".format(response.status_code, url))

    content = json.loads(response.content)["result"]
    hits = content["hits"]
    logger.debug("Hits from response: {}".format(hits))
    if int(hits["@total"]) == 0:
        return []
    return [Publication(hit) for hit in hits["hit"]]


def ask_user_for_publication(publications):
    if len(publications) == 1:
        # There is no selection for the user. Return result.
        return publications[0]

    for i in range(len(publications)):
        print("-" * 3 + " {} ".format(i) + "-" * 17)
        print(publications[i])
        print("-" * 22 + len(str(i)) * "-")
        print()

    while True:
        index = input("Enter number of publication to use: ")
        try:
            index = int(index)
            if index < -1 or index >= len(publications):
                # Trigger help text and continue processing
                raise ValueError()
            if index == -1:
                return None
            break  # Valid input!
        except ValueError:
            print("{} is not a number or is out of range! Range is {} - {}.\n"
                  "Print -1 to abort.".format(index, 0, len(publications) - 1))
            continue
    return publications[index]


def load_bibitem(publication, curlify, copy_to_clipboard, pretty):
    bib_url = publication.url + ".bib"

    logger.info("URL: {}".format(publication.url))
    logger.info("BIB-URL: {}".format(bib_url))

    response = requests.get(bib_url)
    bib = response.content.decode("UTF-8")

    if curlify or pretty:
        bib_database = bibtexparser.loads(bib)

        # We only have one single entry -> [0]
        bib_entry = bib_database.entries[0]

        if curlify:
            # Add extra curly brackets to title
            if "title" in bib_entry:
                title = bib_entry["title"]
                bib_entry["title"] = "{{{}}}".format(title)

        attributes_order = bib_util.get_bibtex_order()

        if pretty:
            hide_attributes = bib_util.get_attribute_names_to_hide()

            hide_prefix = bib_util.get_config("style", "hidePrefix")
            for hide_attribute in hide_attributes:
                if hide_attribute not in bib_entry:
                    # Nothing to hide if attribute is not contained in the BIBTeX
                    continue

                new_hidden_attribute = hide_prefix + hide_attribute
                while new_hidden_attribute in bib_entry:
                    # The attribute exists twice, once as visible and once as hidden.
                    # We don't want to override/delete any element.
                    # Add more prefixes until a non-existing hidden attribute name is found.
                    new_hidden_attribute = hide_prefix + new_hidden_attribute

                bib_entry[new_hidden_attribute] = bib_entry[hide_attribute]
                del bib_entry[hide_attribute]

                # Keep the order of elements in sync
                attributes_order = [new_hidden_attribute if ele == hide_attribute else ele for ele in attributes_order]

        # Apply BIB-Item style
        writer = BibTexWriter()
        writer.indent = " " * 2
        writer.order_entries_by = None
        writer.align_values = True

        if bib_util.get_config("style", "sort"):
            # Order items
            writer.display_order = attributes_order

        bib = writer.write(bib_database)

    if copy_to_clipboard:
        bib_util.copy_to_clipboard(bib)

    print(bib)


def find(title, curlify, copy_to_clipboard, pretty):
    publications_url = bib_util.get_config("settings", "search", "publicationUrl")
    publications_url = publications_url.format(title)  # Set title as query in  URL

    publications = load_publications(publications_url)

    if len(publications) == 0:
        print("No publications found for title: {}".format(title))
        return

    publication = ask_user_for_publication(publications)

    if publication:
        load_bibitem(publication, curlify, copy_to_clipboard, pretty)
