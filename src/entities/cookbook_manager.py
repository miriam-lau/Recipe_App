from entities.cookbook import Cookbook
from pathlib import Path

COOKBOOKS_FILES = ["/Users/miriamlau/Dropbox/RecipeApp/cookbooks.txt", "/home/james/Dropbox/RecipeApp/cookbooks.txt"]


def _get_cookbook_file():
    for cookbook_filename in COOKBOOKS_FILES:
        cookbook_file = Path(cookbook_filename)
        if cookbook_file.is_file():
            return cookbook_filename
    return ""


class CookbookManager:

    def __init__(self):
        self._cookbooks = {}

    @staticmethod
    def create_and_initialize_cookbook_manager(filename: str=_get_cookbook_file()):
        cookbook_manager = CookbookManager()
        cookbook_file = open(filename, "r")
        for cookbook_line in cookbook_file:
            if cookbook_line.strip("\n"):
                cookbook = Cookbook.from_line(cookbook_line)
                cookbook_manager.add_existing_cookbook(cookbook)
        cookbook_file.close()
        return cookbook_manager

    # Adds cookbooks that already have an id.
    def add_existing_cookbook(self, cookbook: Cookbook):
        assert cookbook.id is not None, "Cookbook id should not be None"
        self._cookbooks[cookbook.id] = cookbook

    def add_new_cookbook(self, cookbook: Cookbook, filename: str=_get_cookbook_file()):
        assert cookbook.id is None, "Cookbook id should be None"
        cookbook_id = self._generate_cookbook_id()
        cookbook.id = cookbook_id
        self._cookbooks[cookbook_id] = cookbook
        self._write_cookbooks_to_file(filename)

    def _write_cookbooks_to_file(self, filename: str):
        with open(filename, "w") as f:
            for cookbook in sorted(self._cookbooks.values(), key=lambda cookbook: cookbook.id):
                f.write(cookbook.to_line())
            f.write("\n")

    def _generate_cookbook_id(self):
        i = 1
        while i in self._cookbooks:
            i += 1
        return i

    def get_cookbooks(self):
        return sorted(self._cookbooks.values(), key=lambda cookbook: cookbook.name.lower())

    def get_cookbook(self, id: int):
        return self._cookbooks[id]
