import pyperclip

import config
from bibhelper.handler.bibtex_handler import hide_attributes
from bibhelper.handler.latex_handler import curlify, extract_booktitle_shortname


def rewrite_booktitle(bib_entry: dict) -> None:
    key = "booktitle"
    if key not in bib_entry:
        return

    # Get existing booktitle and extract shortname (e.g. ICDE, SIGMOD, ...)
    booktitle = bib_entry[key]
    booktitle_shortname = extract_booktitle_shortname(booktitle)

    if booktitle_shortname is None:
        return

    # Create new booktitle based on configuration. E.g. Configuration is: "Proc.\ {}" and new title will be:
    # E.g. "Proc.\ ICDE"
    new_booktitle_placeholder = config.get_config_property("style", "rewriteBooktitle", "nameWithPlaceholder")
    new_booktitle = new_booktitle_placeholder.format(booktitle_shortname)

    # Now we have to hide the old booktitle and create a new entry
    hide_prefix = config.get_hide_prefix()

    # Search for a new name of the original entry:
    # E.g. booktitle = "In Proceedings of ICDE...."
    # And we want to create two entries out of this (hide prefix set to "_"):
    # _booktitle = "In Proceedings of ICDE...."
    # booktitle = "Proc.\ ICDE"
    non_existing_booktitle_entry = key
    while non_existing_booktitle_entry in bib_entry:
        if bib_entry[non_existing_booktitle_entry] == new_booktitle:
            # Abort if our new booktitle is already present. We do not create duplicates...
            return
        non_existing_booktitle_entry = hide_prefix + non_existing_booktitle_entry

    # Create new entry for original value
    bib_entry[non_existing_booktitle_entry] = bib_entry[key]
    # Set the new booktitle
    bib_entry[key] = new_booktitle


def hide_attributes(bib_entry: dict):
    hide_prefix = config.get_hide_prefix()
    attributes_to_hide = config.get_attribute_names(hidden_only=True)
    hide_attributes(bib_entry, attributes_to_hide, hide_prefix)


def curlify_title(bib_entry: dict):
    key = "title"
    if key in bib_entry:
        bib_entry[key] = curlify(bib_entry[key])


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def read_from_clipboard() -> str:
    return pyperclip.paste()
