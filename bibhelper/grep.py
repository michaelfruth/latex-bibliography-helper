from difflib import SequenceMatcher

from bibhelper.handler import bibtex_handler
from bibhelper import config
from bibtexparser.bibdatabase import BibDatabase


def output_result(entry_with_similarity):
    entry, similarity = entry_with_similarity
    print("Found match with similarity of {} (1 is max.).".format(similarity))

    writer = bibtex_handler.get_bibtex_writer()
    writer.display_order = config.get_attribute_names()
    bib_database = BibDatabase()
    bib_database.entries = [entry]
    bib = writer.write(bib_database)
    print(bib.strip())
    print()
    print("Key is: {}".format(entry["ID"]))


def grep(content: str, keyword_to_search: [str], output_highest_similarity: bool) -> None:
    bib_database = bibtex_handler.load_bibtex_database(content)

    if len(bib_database.entries) == 0:
        print("Could not find/load any BibTeX entries for content:\n{}".format(content))
        exit(1)

    entries_with_similarity = []
    for entry in bib_database.entries:
        # Find for entry highest similarity
        highest_similarity = -1
        for key, value in entry.items():
            if keyword_to_search in value:
                # If keyword is contained in value
                similarity = 1
            else:
                # Otherwise compute similiarty
                similarity = SequenceMatcher(None, value, keyword_to_search).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity

        # Save entry with similarity for later processing
        entries_with_similarity.append((entry, highest_similarity))

    # Sort based on highest similarity
    entries_with_similarity.sort(key=lambda x: x[1], reverse=True)
    if output_highest_similarity:
        output_result(entries_with_similarity[0])
