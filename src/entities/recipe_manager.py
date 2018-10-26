from .recipe import Recipe
import csv
from .files.files import write_entities_to_file
import os

from src.settings.settings import Settings

PROD_FILE  = "Recipe Database - recipes.csv"
DEBUG_FILE = "Recipe Database - recipes (copy).csv"


class RecipeManager:

    def __init__(self, settings: Settings):
        self._recipes = {}
        self._settings = settings

    def get_recipes_file(self):
        file_prefix = self._settings.recipe_app_directory
        file_postfix = DEBUG_FILE if self._settings.debug_mode else PROD_FILE
        return file_prefix + file_postfix

    @staticmethod
    def create_and_initialize_recipe_manager(cookbook_manager, settings: Settings):
        recipe_manager = RecipeManager(settings)
        with open(recipe_manager.get_recipes_file(), 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for recipe_values in csv_reader:
                recipe = Recipe.from_values(recipe_values)
                recipe_manager.add_existing_recipe(cookbook_manager, recipe)
        return recipe_manager

    # Adds recipes that already have an id.
    def add_existing_recipe(self, cookbook_manager, recipe: Recipe):
        assert recipe.id is not None, "Recipe id should not be None"
        self._recipes[recipe.id] = recipe
        cookbook_manager.get_cookbook(recipe.cookbook_id).add_recipe(recipe)

    def add_new_recipe(self, cookbook_manager, cookbook_id: str, name: str, priority: str, category: str, notes: str) \
            -> Recipe:
        recipe_id = self._generate_recipe_id()
        recipe = Recipe(recipe_id, int(cookbook_id), name, int(priority) if priority else 0, \
                        False, category, notes)
        self._recipes[recipe_id] = recipe
        cookbook_manager.get_cookbook(recipe.cookbook_id).add_recipe(recipe)
        self._write_recipes_to_file()
        return recipe

    def modify_recipe(self, id: int, name: str, category: str, priority: int, has_image: bool, notes: str):
        recipe = self.get_recipe(id)
        recipe.name = name
        recipe.category = category
        recipe.priority = priority
        recipe.has_image = has_image
        if not has_image:
            image_filename = recipe.get_image_filename(self._settings)
            if os.path.exists(image_filename):
                os.remove(image_filename)
        recipe.notes = notes
        self._write_recipes_to_file()

    # file is of type file found in flask
    def upload_recipe_image(self, id: int, file):
        recipe = self.get_recipe(id)
        file.save(recipe.get_image_filename(self._settings))
        recipe.has_image = True
        self._write_recipes_to_file()

    def delete_recipe(self, cookbook_manager, entry_manager, id: int):
        recipe = self.get_recipe(id)
        recipe_entries = []
        for entry in recipe.entries:
            recipe_entries.append(entry)
        for entry in recipe_entries:
            entry_manager.delete_entry(self, entry.id)
        cookbook_manager.get_cookbook(recipe.cookbook_id).remove_recipe(recipe)
        del self._recipes[id]
        self._write_recipes_to_file()

    def _write_recipes_to_file(self):
        write_entities_to_file(self.get_recipes_file(), self._recipes.values())

    def _generate_recipe_id(self):
        i = 1
        while i in self._recipes:
            i += 1
        return i

    def get_recipes(self):
        return sorted(self._recipes.values(), key=lambda recipe: recipe.name.lower())

    def get_recipe(self, id: int):
        return self._recipes[id]
