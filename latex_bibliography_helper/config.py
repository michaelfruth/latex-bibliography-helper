_config = None
_default_config = {
    "settings": {
        "search": {
            "publicationUrl": "http://dblp.org/search/publ/api?q={}&format=json",
            "authorUrl": "http://dblp.org/search/author/api?q={}&format=json",
            "venueUrl": "http://dblp.org/search/venue/api?q={}&format=json"
        }
    },
    "style": {
        "hidePrefix": "_",
        "sort": True,
        "rewriteBooktitle": {
            "rewrite": True,
            "nameWithPlaceholder": "Proc.\\ {}"
        },
        "attributes": []
    }
}


def get_hide_prefix() -> str:
    return get_config_property("style", "hidePrefix")


def is_sort_attributes() -> bool:
    return get_config_property("style", "sort")


def is_rewrite_booktitle() -> bool:
    return get_config_property("style", "rewriteBooktitle", "rewrite")


def get_attribute_names(hidden_only: bool = False) -> [str]:
    """
    Returns the names of all attributes. If 'only_hide' is set to true, only the attribute names for which the hide
    property is set to true will be returned.
    """

    # "attributes" : [
    #   "author",
    #   { "name": "author", "hide": True/False, ...}
    # ]
    attributes = get_config_property("style", "attributes")

    if hidden_only:
        # Keep only hidden attributes
        attributes = [a for a in attributes if isinstance(a, dict) and a["hide"] is True]

    names = []
    for attribute in attributes:
        if isinstance(attribute, dict):
            names.append(attribute["name"])
        else:
            names.append(attribute)
    return names


def get_config_property(*args):
    current_element = _config

    for arg in args:
        if not isinstance(current_element, dict):
            raise TypeError("Trying to access a non-dictionary configuration element by key: '{}'.\n"
                            "Element: {}".format(arg, current_element))
        if arg not in current_element:
            raise ValueError("Could not find/access attribute '{}' in configuration.\n"
                             "Current element: '{}'".format(arg, current_element))

        current_element = current_element[arg]

    return current_element


def set_config_or_default(config=None):
    global _config
    _config = config if config is not None else _default_config
