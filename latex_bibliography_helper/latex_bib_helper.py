import json
import logging
import pkgutil

import jsonschema

import util

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare(config_file):
    # Load
    json_schema = json.loads(pkgutil.get_data("latex_bib_helper", "resources/config.schema.json"))
    config = json.load(config_file)

    # Validate
    try:
        jsonschema.validate(config, json_schema)
        util.set_config_or_default(config)
    except jsonschema.exceptions.ValidationError as e:
        logger.warning("Failed validating the configuration file.\n{}\n"
                       "Using the default configuration.".format(e))
        util.set_config_or_default()

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
    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="Verbose output")

    subparsers = parser.add_subparsers(dest='command',
                                       help="The functionality to use.",
                                       required=True)

    find_parser = subparsers.add_parser("Find")
    find_parser.add_argument("--pretty",
                             dest="pretty",
                             help="Apply the style (order, hide) of attributes specified in the configuration file.",
                             action="store_true")
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
                                    dest="input_clipboard",
                                    action="store_true",
                                    help="Use the clipboard")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    prepare(args.config_file)

    if args.command == "Find":
        import find

        title = " ".join(args.title)
        find.find(title, args.curlify, args.copy_to_clipboard, args.pretty)
    elif args.command == "Beautify":
        import beautify

        if args.input_clipboard:
            file_content = util.read_from_clipboard()
        else:
            input_file = args.input_file
            file_content = input_file.read()
            input_file.close()
        beautify.beautify(file_content, args.curlify, args.copy_to_clipboard)
    else:
        raise ValueError("Unknown ArgumentParser option: {}".format(args.command))
