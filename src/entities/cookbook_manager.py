from .cookbook import Cookbook
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from ..settings import settings

COOKBOOKS_FILE_PREFIXES = ["/Users/miriamlau", "/home/james"]
DROPBOX_FILE = "/Dropbox/RecipeApp/"
PROD_COOKBOOKS_FILE_POSTFIX = "Recipe Database - cookbooks.csv"
DEBUG_COOKBOOKS_FILE_POSTFIX = "Recipe Database - cookbooks (copy).csv"


def _get_cookbook_file():
    cookbooks_filename = ""
    cookbooks_file_postfix = DEBUG_COOKBOOKS_FILE_POSTFIX if settings.get_debug_mode() else PROD_COOKBOOKS_FILE_POSTFIX
    for cookbooks_file_prefix in COOKBOOKS_FILE_PREFIXES:
        cookbooks_filename = cookbooks_file_prefix + DROPBOX_FILE + cookbooks_file_postfix
        cookbook_file = Path(cookbooks_filename)
        if cookbook_file.is_file():
            return cookbooks_filename
    return ""


class CookbookManager:

    def __init__(self):
        self._cookbooks = {}

    @staticmethod
    def create_and_initialize_cookbook_manager(filename: str=_get_cookbook_file()):
        cookbook_manager = CookbookManager()
        with open(filename) as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for cookbook_values in csv_reader:
                cookbook = Cookbook.from_values(cookbook_values)
                cookbook_manager.add_existing_cookbook(cookbook)
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

    def modify_cookbook(self, id: int, name: str, notes: str, filename: str=_get_cookbook_file()):
        cookbook = self.get_cookbook(id)
        cookbook.name = name
        cookbook.notes = notes
        self._write_cookbooks_to_file(filename)

    def delete_cookbook(self, recipe_manager, entry_manager, id: int, filename: str=_get_cookbook_file()):
        cookbook = self.get_cookbook(id)
        cookbook_recipes = []
        for recipe in cookbook.recipes:
            cookbook_recipes.append(recipe)
        for recipe in cookbook_recipes:
            recipe_manager.delete_recipe(self, entry_manager, recipe.id)
        del self._cookbooks[id]
        self._write_cookbooks_to_file(filename)

    def _write_cookbooks_to_file(self, filename: str):
        with atomic_write(filename, keep=False) as f:
            writer = csv.writer(f, dialect=csv.excel)
            for cookbook in sorted(self._cookbooks.values(), key=lambda cookbook: cookbook.id):
                writer.writerow(cookbook.to_tuple())

    def _generate_cookbook_id(self):
        i = 1
        while i in self._cookbooks:
            i += 1
        return i

    def get_cookbooks(self):
        return sorted(self._cookbooks.values(), key=lambda cookbook: cookbook.name.lower())

    def get_cookbook(self, id: int):
        return self._cookbooks[id]
