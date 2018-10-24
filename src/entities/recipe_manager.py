from entities.recipe import Recipe
from pathlib import Path
import csv

RECIPE_FILES = ["/Users/miriamlau/Dropbox/RecipeApp/recipes.csv", "/home/james/Dropbox/RecipeApp/recipes.csv"]


def _get_recipe_file():
    for recipe_filename in RECIPE_FILES:
        recipe_file = Path(recipe_filename)
        if recipe_file.is_file():
            return recipe_filename
    return ""


class RecipeManager:

    def __init__(self):
        self._recipes = {}

    @staticmethod
    def create_and_initialize_recipe_manager(filename: str=_get_recipe_file()):
        recipe_manager = RecipeManager()
        with open(filename, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for recipe_values in csv_reader:
                recipe = Recipe.from_values(recipe_values)
                recipe_manager.add_existing_recipe(recipe)
        return recipe_manager

    # Adds recipes that already have an id.
    def add_existing_recipe(self, recipe: Recipe):
        assert recipe.id is not None, "Recipe id should not be None"
        self._recipes[recipe.id] = recipe

    def add_new_recipe(self, recipe: Recipe, filename: str=_get_recipe_file()):
        assert recipe.id is None, "Recipe id should be None"
        recipe_id = self._generate_recipe_id()
        recipe.id = recipe_id
        self._recipes[recipe_id] = recipe
        self._write_recipes_to_file(filename)

    def _write_recipes_to_file(self, filename: str):
        with open(filename, "w") as f:
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

    def get_recipes_for_cookbook(self, id: int):
        recipes = self._recipes.values()
        recipes = filter(lambda recipe: recipe.cookbook_id == id, recipes)
        return sorted(recipes, key=lambda recipe: recipe.name.lower())

    def get_recipe(self, id: int):
        return self._recipes[id]
