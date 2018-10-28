import sys
from pathlib import Path


DROPBOX_FILE_PREFIXES = ["/Users/miriamlau", "/Users/jameslee", "/home/james"]
DROPBOX_FILE = "/Dropbox/RecipeApp/"


class Settings:

    def __init__(self):
        self.recipe_app_directory = self._get_recipe_app_directory()
        self._debug_mode = self._get_debug_mode()

    def _get_recipe_app_directory(self):
        for recipes_file_prefix in DROPBOX_FILE_PREFIXES:
            recipes_directory = recipes_file_prefix + DROPBOX_FILE
            recipe_file = Path(recipes_directory)
            try:
                if recipe_file.is_dir():
                    return recipes_directory
            except IOError:
                print("An error occurred trying to open %s", recipe_file)
        raise ValueError("A valid dropbox directory could not be found")

    def _get_debug_mode(self):
        debug_mode = False
        for arg in sys.argv:
            if arg == "--debugger":
                debug_mode = True
        return debug_mode

    @property
    def debug_mode(self):
        return self._debug_mode
