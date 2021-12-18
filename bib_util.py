import pyperclip

_config = None


def get_config(*args):
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


def set_config(config):
    global _config
    _config = config


def get_bib_order():
    with open('pretty-order.txt', 'r') as f:
        return [f.strip() for f in f.readlines() if len(f.strip()) > 0]


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def copy_from_clipboard() -> str:
    return pyperclip.paste()
