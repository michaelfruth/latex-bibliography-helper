import pyperclip

config = {
    "attributes": []
}


def load_or_default_config(config_file) -> None:
    global config


def get_bib_order():
    with open('pretty-order.txt', 'r') as f:
        return [f.strip() for f in f.readlines() if len(f.strip()) > 0]


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def copy_from_clipboard() -> str:
    return pyperclip.paste()
