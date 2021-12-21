import pyperclip

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
        "attributes": []
    }
}


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


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def read_from_clipboard() -> str:
    return pyperclip.paste()
