import requests
import json
import subprocess

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

DBLP_BASE_URL = "http://dblp.org/search/"
DBLP_PUBLICATION_URL = DBLP_BASE_URL + "publ/api?q={}&format=json"
DBLP_AUTHOR_URL = DBLP_BASE_URL + "author/api?q={}&format=json"
DBLP_VENUE_URL = DBLP_BASE_URL + "venue/api?q={}&format=json"


def load_publications(url):
    logger.info("Fetching {}".format(url))

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(url)

    content = json.loads(response.content)["result"]
    hits = content["hits"]
    if int(hits["@total"]) == 0:
        return []
    return [Publication(hit) for hit in hits["hit"]]


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


def load_bibitem(publication):
    response = requests.get(publication.url + ".bib")

    bib = response.content.decode("UTF-8")

    # TODO: This is MacOS specifc only"
    subprocess.run("pbcopy", universal_newlines=True, input=bib)

    print(bib)
    print("Copied to clipboard!")


def user_select_publication(publications):
    if len(publications) == 1:
        return publications[0]
    for i in range(len(publications)):
        print("-" * 3 + " {} ".format(i) + "-" * 17)
        print(publications[i])
        print("-" * 22 + len(str(i)) * "-")
        print()

    while True:
        index = input("Number of BIB to collect: ")
        try:
            index = int(index)
            if index < -1 or index >= len(publications):
                # Just to trigger the help text and continue processing
                raise ValueError()
            if index == -1:
                return None
            break  # Valid input!
        except ValueError:
            print("{} is not a number or is out of range! Range is {} - {}.\n"
                  "Print -1 to abort.".format(index, 0, len(publications) - 1))
            continue
    return publications[index]


def main(title):
    publications = load_publications(DBLP_PUBLICATION_URL.format(title))

    if len(publications) == 0:
        print("No publications found for title: {}".format(title))
        return

    publication = user_select_publication(publications)

    if publication is not None:
        load_bibitem(publication)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("title", help="Title of publication.")
    args = parser.parse_args()

    title_to_find = args.title
    main(title_to_find)
