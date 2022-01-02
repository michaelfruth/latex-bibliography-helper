import json
import logging

import bibtexparser
import requests
from bibtexparser.bwriter import BibTexWriter

import config
import util
from handler import bibtex_handler

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


class Author:
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


def load_bibitem(publication, curlify, pretty):
    bib_url = publication.url + ".bib"

    logger.info("URL: {}".format(publication.url))
    logger.info("BIB-URL: {}".format(bib_url))

    response = requests.get(bib_url)
    bib = response.content.decode("UTF-8")

    if not curlify and not pretty:
        # Return result of URL immediately. No processing by BIBTeX-Parser needed.
        return bib

    bib_database = bibtexparser.loads(bib)

    # We only have one single entry -> [0]
    bib_entry = bib_database.entries[0]

    if curlify:
        util.curlify_title(bib_entry)
    if pretty:
        util.hide_attributes(bib_entry)
        if config.is_rewrite_booktitle():
            util.rewrite_booktitle(bib_entry)

    writer = BibTexWriter()
    bibtex_handler.apply_bibtex_writer_style(writer)

    attributes_order = writer.display_order
    if config.is_sort_attributes():
        # Order attributes
        attributes_order = bibtex_handler.create_attributes_order(bib_entry.keys(),
                                                                  config.get_attribute_names(),
                                                                  config.get_hide_prefix())
    writer.display_order = attributes_order

    bib = writer.write(bib_database)
    return bib


def find(title, curlify, copy_to_clipboard, pretty):
    publications_url = config.get_config_property("settings", "search", "publicationUrl")
    publications_url = publications_url.format(title)  # Set title as query in  URL

    publications = load_publications(publications_url)

    if len(publications) == 0:
        print("No publications found for title: {}".format(title))
        return

    publication = ask_user_for_publication(publications)

    if publication:
        item = load_bibitem(publication, curlify, pretty)

        if copy_to_clipboard:
            util.copy_to_clipboard(item)
        print(item)
