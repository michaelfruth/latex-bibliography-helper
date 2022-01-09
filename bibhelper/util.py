import pyperclip


def copy_to_clipboard(content) -> None:
    pyperclip.copy(content)


def read_from_clipboard() -> str:
    return pyperclip.paste()
