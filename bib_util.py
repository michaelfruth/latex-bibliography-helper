import subprocess


def get_bib_order():
    with open('pretty-order.txt', 'r') as f:
        return [f.strip() for f in f.readlines() if len(f.strip()) > 0]


def copy_to_clipboard(input):
    # TODO: This is MacOS specific only"
    subprocess.run("pbcopy", universal_newlines=True, input=input)
