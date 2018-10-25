from .recipe import Recipe
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from .cookbook_manager import CookbookManager
import os

from src.settings import settings

PROD_FILE  = "Recipe Database - recipes.csv"
DEBUG_FILE = "Recipe Database - recipes (copy).csv"


def _get_recipe_file():
    file_prefix = settings.get_dropbox_directory()
    file_postfix = DEBUG_FILE if settings.get_debug_mode() else PROD_FILE
    return file_prefix + file_postfix


class RecipeManager:

    def __init__(self):
        self._recipes = {}

    @staticmethod
    def create_and_initialize_recipe_manager(cookbook_manager, filename: str=_get_recipe_file()):
        recipe_manager = RecipeManager()
        with open(filename, 'rt') as csvfile:
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

    def add_new_recipe(self, cookbook_manager, recipe: Recipe, filename: str=_get_recipe_file()):
        assert recipe.id is None, "Recipe id should be None"
        recipe_id = self._generate_recipe_id()
        recipe.id = recipe_id
        self._recipes[recipe_id] = recipe
        cookbook_manager.get_cookbook(recipe.cookbook_id).add_recipe(recipe)
        self._write_recipes_to_file(filename)

    def modify_recipe(self, id: int, name: str, category: str, priority: int, has_image: bool, notes: str, \
                      filename: str=_get_recipe_file()):
        recipe = self.get_recipe(id)
        recipe.name = name
        recipe.category = category
        recipe.priority = priority
        recipe.has_image = has_image
        if not has_image:
            image_filename = recipe.get_image_filename()
            if os.path.exists(image_filename):
                os.remove(image_filename)
        recipe.notes = notes
        self._write_recipes_to_file(filename)

    # file is of type file found in flask
    def upload_recipe_image(self, id: int, file, filename: str=_get_recipe_file()):
        recipe = self.get_recipe(id)
        file.save(recipe.get_image_filename())
        recipe.has_image = True
        self._write_recipes_to_file(filename)

    def delete_recipe(self, cookbook_manager, entry_manager, id: int, filename: str=_get_recipe_file()):
        recipe = self.get_recipe(id)
        recipe_entries = []
        for entry in recipe.entries:
            recipe_entries.append(entry)
        for entry in recipe_entries:
            entry_manager.delete_entry(self, entry.id)
        cookbook_manager.get_cookbook(recipe.cookbook_id).remove_recipe(recipe)
        del self._recipes[id]
        self._write_recipes_to_file(filename)

    def _write_recipes_to_file(self, filename: str):
        with atomic_write(filename, keep=False) as f:
            writer = csv.writer(f, dialect=csv.excel)
            for recipe in sorted(self._recipes.values(), key=lambda recipe: recipe.id):
                writer.writerow(recipe.to_tuple())

    def _generate_recipe_id(self):
        i = 1
        while i in self._recipes:
            i += 1
        return i

    def get_recipes(self):
        return sorted(self._recipes.values(), key=lambda recipe: recipe.name.lower())

    def get_recipe(self, id: int):
        return self._recipes[id]
