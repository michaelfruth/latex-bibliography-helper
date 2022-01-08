import json
import logging
import os
import pkgutil
from argparse import ArgumentParser, FileType
from pathlib import Path

import jsonschema

from bibhelper.config import set_config
from bibhelper.util import read_from_clipboard

logger = logging.getLogger(__name__)

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE_DEFAULT_NAME = ".latex_bibtex_helper_config.json"
CONFIG_FILE_ENV_NAME = "LATEX_BIBTEX_HELPER_CONFIG"
CONFIG_FILE_HOME_NAME = CONFIG_FILE_DEFAULT_NAME


def load_configuration(config_file_args: str) -> None:
    # Configuration file priority:
    # 1. Argument: --config
    # 2. environment variable
    # 3. home directory
    # 4. default
    if CONFIG_FILE_ENV_NAME in os.environ:
        config_file_env = os.environ[CONFIG_FILE_ENV_NAME]
    else:
        config_file_env = None
    config_file_home = os.path.join(Path.home(), CONFIG_FILE_HOME_NAME)
    config_file_default = os.path.join(SCRIPT_DIRECTORY, CONFIG_FILE_HOME_NAME)

    # Order configuration files
    configuration_files = [config_file_args,
                           config_file_env,
                           config_file_home,
                           config_file_default]

    # Try to load/set configuration file
    is_config_set = False
    for config_file in configuration_files:
        if try_load_and_set_config(config_file):
            is_config_set = True
            break

    if not is_config_set:
        # Could not set/load a configuration file. Exit.
        print("Could not find a suitable configuration file. Please specify a configuration file to continue.\n"
              "Tried to load configuration files (same order is used to load the configuration file):\n"
              f"1. Command line argument: --config\n"
              f"2. Environment variable: {CONFIG_FILE_ENV_NAME}\n"
              f"3. Configuration file in home directory: {config_file_home}\n"
              f"4. Default configuration file: {config_file_default}")
        exit(1)


def try_load_and_set_config(config_file: str) -> bool:
    logger.debug(f"Trying to load configuration file: {config_file}")
    if config_file is None or not os.path.isfile(config_file):
        return False

    with open(config_file, "r") as f:
        # Load config file
        json_config = json.load(f)
    # Load schema
    json_schema = json.loads(pkgutil.get_data(__name__, "resources/config.schema.json"))

    # Validate
    try:
        jsonschema.validate(json_config, json_schema)
        set_config(json_config)
        logger.debug(f"Loaded configuratil file {config_file} successfully.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.warning("Failed validating the configuration file.\n{}\n"
                       "Using the default configuration.".format(e))
        return False


def main():
    parser = ArgumentParser(
        description="This is a tool to help in setting up, cleaning and refactoring the LaTex bibliography.")
    parser.add_argument("--config",
                        dest="config_file",
                        help="The configuration file to be used.")
    parser.add_argument("--curly",
                        dest="curlify",
                        action="store_true",
                        help="Set another pair of curly brackets around the title")
    parser.add_argument("--pretty",
                        dest="pretty",
                        help="Apply the style (order, hide) of attributes specified in the configuration file.",
                        action="store_true")
    parser.add_argument("-ctc", "--copy-to-clipboard",
                        dest="copy_to_clipboard",
                        action="store_true",
                        help="Copy the result into the clipboard.")
    parser.add_argument("-v", "--verbose",
                        action="store_const",
                        dest="loglevel",
                        const=logging.INFO,
                        help="Print verbose output"
                        )
    parser.add_argument('-d', '--debug',
                        help="Print debugging statements",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.WARNING,
                        )

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
                                    dest="input_clipboard",
                                    action="store_true",
                                    help="Use the clipboard")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    load_configuration(args.config_file)

    if args.command == "Find":
        import find

        title = " ".join(args.title)
        find.find(title, args.curlify, args.copy_to_clipboard, args.pretty)
    elif args.command == "Beautify":
        import beautify

        if args.input_clipboard:
            beautify_content = read_from_clipboard()
        else:
            input_file = args.input_file
            beautify_content = input_file.read()
            input_file.close()
        beautify.beautify(beautify_content, args.curlify, args.copy_to_clipboard, args.pretty)
    else:
        raise ValueError("Unknown ArgumentParser option: {}".format(args.command))


if __name__ == "__main__":
    main()
