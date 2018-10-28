from .recipe import Recipe
from .entity_manager import EntityManager
from typing import Tuple
import os

from src.settings.settings import Settings

PROD_FILE  = "Recipe Database - recipes.csv"
DEBUG_FILE = "Recipe Database - recipes (copy).csv"


class RecipeManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Recipe, settings, PROD_FILE, DEBUG_FILE)

    def get_recipes(self):
        return self._get_entities()

    def get_recipe(self, entity_id: int):
        return self.get_entity(entity_id)

    # file is of type file found in flask
    def upload_recipe_image(self, entity_id: int, file):
        recipe = self.get_entity(entity_id)
        file.save(recipe.get_image_filename(self._settings))
        recipe.has_image = True
        self.write_entities_to_file()

    def modify_recipe(self, id: int, values: Tuple[str]):
        self.modify_entity(id, values)
        if values[2].lower() == 'false':
            image_filename = self.get_entity(id).get_image_filename(self._settings)
            if os.path.exists(image_filename):
                os.remove(image_filename)
