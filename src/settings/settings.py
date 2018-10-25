import sys
from pathlib import Path


DROPBOX_FILE_PREFIXES = ["/Users/miriamlau", "/home/james"]
DROPBOX_FILE = "/Dropbox/RecipeApp/"


def get_dropbox_directory():
    recipes_filename = ""
    for recipes_file_prefix in DROPBOX_FILE_PREFIXES:
        recipes_directory = recipes_file_prefix + DROPBOX_FILE
        recipe_file = Path(recipes_directory)
        if recipe_file.is_dir():
            return recipes_directory


def get_debug_mode():
    debug_mode = False
    for arg in sys.argv:
        if arg == "--debugger":
            debug_mode = True
    return debug_mode

