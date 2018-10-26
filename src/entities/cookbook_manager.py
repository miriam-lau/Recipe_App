from .cookbook import Cookbook
from .files.files import write_entities_to_file
from src.settings.settings import Settings
import csv

PROD_FILE = "Recipe Database - cookbooks.csv"
DEBUG_FILE = "Recipe Database - cookbooks (copy).csv"


class CookbookManager:

    def __init__(self, settings: Settings):
        self._cookbooks = {}
        self._settings = settings

    def get_cookbooks_file(self):
        file_prefix = self._settings.recipe_app_directory
        file_postfix = DEBUG_FILE if self._settings.debug_mode else PROD_FILE
        return file_prefix + file_postfix

    @staticmethod
    def create_and_initialize_cookbook_manager(settings: Settings):
        cookbook_manager = CookbookManager(settings)
        with open(cookbook_manager.get_cookbooks_file()) as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for cookbook_values in csv_reader:
                cookbook = Cookbook.from_values(cookbook_values)
                cookbook_manager.add_existing_cookbook(cookbook)
        return cookbook_manager

    # Adds cookbooks that already have an id.
    def add_existing_cookbook(self, cookbook: Cookbook):
        assert cookbook.id is not None, "Cookbook id should not be None"
        self._cookbooks[cookbook.id] = cookbook

    def add_new_cookbook(self, name, notes) -> Cookbook:
        cookbook_id = self._generate_cookbook_id()
        cookbook = Cookbook(cookbook_id, name, notes)
        self._cookbooks[cookbook_id] = cookbook
        self._write_cookbooks_to_file()
        return cookbook

    def modify_cookbook(self, id: int, name: str, notes: str):
        cookbook = self.get_cookbook(id)
        cookbook.name = name
        cookbook.notes = notes
        self._write_cookbooks_to_file()

    def delete_cookbook(self, recipe_manager, entry_manager, id: int):
        cookbook = self.get_cookbook(id)
        cookbook_recipes = []
        for recipe in cookbook.recipes:
            cookbook_recipes.append(recipe)
        for recipe in cookbook_recipes:
            recipe_manager.delete_recipe(self, entry_manager, recipe.id)
        del self._cookbooks[id]
        self._write_cookbooks_to_file()

    def _generate_cookbook_id(self):
        i = 1
        while i in self._cookbooks:
            i += 1
        return i

    def get_cookbooks(self):
        return sorted(self._cookbooks.values(), key=lambda cookbook: cookbook.name.lower())

    def get_cookbook(self, id: int):
        return self._cookbooks[id]

    def _write_cookbooks_to_file(self):
        write_entities_to_file(self.get_cookbooks_file(), self._cookbooks.values())
