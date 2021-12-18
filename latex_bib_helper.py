from os import path
import bib_util
import json


def prepare(config_file):
    config = json.load(config_file)
    bib_util.set_config(config)
    config_file.close()


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(
        description="This is a tool to help in setting up, cleaning and refactoring the LaTex bibliography.")
    parser.add_argument("--config",
                        dest="config_file",
                        type=FileType('r', encoding='UTF-8'),
                        help="The configuration file to be used.",
                        default="config.json")
    parser.add_argument("-c", "--curly",
                        dest="curlify",
                        action="store_true",
                        help="Set another pair of curly brackets around the tile")
    parser.add_argument("-ctc", "--copy-to-clipboard",
                        dest="copy_to_clipboard",
                        action="store_true",
                        help="Copy the result into the clipboard.")

    subparsers = parser.add_subparsers(dest='command',
                                       help="The functionality to use.",
                                       required=True)

    find_parser = subparsers.add_parser("Find")
    find_parser.add_argument(dest="title",
                             help="Title of publication.",
                             nargs="+")

    pretty_parser = subparsers.add_parser("Beautify")
    pretty_input_group = pretty_parser.add_mutually_exclusive_group(required=True)
    pretty_input_group.add_argument("-f", "--file",
                                    dest="input_file",
                                    type=FileType('r', encoding='UTF-8'),
                                    help="The file to pretty print")
    pretty_input_group.add_argument("-cfc", "--copy-from-clipboard",
                                    action="store_true",
                                    dest="input_clipboard",
                                    help="Use the clipboard")

    args = parser.parse_args()
    prepare(args.config_file)

    if args.command == "Find":
        pass
    elif args.command == "Beautify":
        pass
    else:
        raise ValueError("Unknown ArgumentParser option: {}".format(args.command))
