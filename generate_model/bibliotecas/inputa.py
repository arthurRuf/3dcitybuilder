import re, logging
from . import path_manager

INPUT_TYPES = {
    "FLOAT": {
        "validate": lambda x: bool(re.compile(r'^[-+]?[-0-9]\d*$').match(x)),
        "convert": lambda x: float(x)
    },
    "INT": {
        "validate": lambda x: bool(re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$').match(x)),
        "convert": lambda x: int(x)
    },
    "STR": {
        "validate": lambda x: True,
        "convert": lambda x: str(x)
    },
    "BOOL": {
        "validate": lambda x: True if x.upper() in ["Y", "YES", "T", "TRUE", "1",
                                                    "N", "NO", "F", "FALSE", "0"] else False,
        "convert": lambda x: True if x.upper() in ["Y", "YES", "T", "TRUE", "1"] else False
    },
    "PATH_CREATABLE": {
        "validate": lambda x: validate_PATH_CREATABLE(x),
        "convert": lambda x: str(x)
    },
    "PATH_READABLE": {
        "validate": lambda x: path_manager.is_path_exists(x),
        "convert": lambda x: str(x)
    },
}


def validate_PATH_CREATABLE(path):
    if path_manager.is_path_exists_or_creatable(path):

        if path_manager.is_path_exists(path):
            overrite = validate("Output file location already exists. Do you want to override it? [yes/no]: ",
                                INPUT_TYPES["BOOL"])

            if not overrite:
                return False
        return True

    return False


def validate(msg, predicate=INPUT_TYPES["STR"], default_value=None, is_mandatory=True, error_string="Illegal Input"):
    while True:
        result = input(msg).strip()

        if (result == "" and default_value != None):
            result = default_value
        if result == "" and is_mandatory:
            continue
        if predicate["validate"](result):
            return predicate["convert"](result)

        logging.error(error_string)
