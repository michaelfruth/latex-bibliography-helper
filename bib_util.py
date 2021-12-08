import pyperclip


def get_bib_order():
    with open('pretty-order.txt', 'r') as f:
        return [f.strip() for f in f.readlines() if len(f.strip()) > 0]


def copy_to_clipboard(input):
    pyperclip.copy(input)


def copy_from_clipboard():
    return pyperclip.paste()
