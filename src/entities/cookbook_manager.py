from .cookbook import Cookbook
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from ..settings import settings

PROD_FILE = "Recipe Database - cookbooks.csv"
DEBUG_FILE = "Recipe Database - cookbooks (copy).csv"


def _get_cookbook_file():
    file_prefix = settings.get_dropbox_directory()
    file_postfix = DEBUG_FILE if settings.get_debug_mode() else PROD_FILE
    return file_prefix + file_postfix


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

    def add_new_cookbook(self, name, notes, filename: str=_get_cookbook_file()):
        cookbook_id = self._generate_cookbook_id()
        cookbook = Cookbook(cookbook_id, name, notes)
        self._cookbooks[cookbook_id] = cookbook
        self._write_cookbooks_to_file(filename)
        return cookbook

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
