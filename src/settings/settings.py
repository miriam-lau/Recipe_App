import sys
from pathlib import Path


# TODO: Needs a test.
class Settings:

    DROPBOX_FILE_PREFIXES = ["/Users/miriamlau", "/Users/jameslee", "/home/james"]
    DROPBOX_FILE = "/Dropbox/RecipeApp/"

    def __init__(self):
        self.recipe_app_directory = Settings._get_recipe_app_directory()
        self._debug_mode = Settings._get_debug_mode()

    @staticmethod
    def _get_recipe_app_directory():
        for recipes_file_prefix in Settings.DROPBOX_FILE_PREFIXES:
            recipes_directory = recipes_file_prefix + Settings.DROPBOX_FILE
            recipe_file = Path(recipes_directory)
            try:
                if recipe_file.is_dir():
                    return recipes_directory
            except IOError:
                pass
        raise ValueError("A valid dropbox directory could not be found")

    @staticmethod
    def _get_debug_mode():
        debug_mode = False
        for arg in sys.argv:
            if arg == "--debugger":
                debug_mode = True
        return debug_mode

    @property
    def debug_mode(self):
        return self._debug_mode
