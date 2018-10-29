from .recipe import Recipe
from .entity_manager import EntityManager
from typing import Dict
import os

from src.settings.settings import Settings

PROD_FILE  = "Recipe Database - recipes.csv"
DEBUG_FILE = "Recipe Database - recipes (copy).csv"


class RecipeManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Recipe, settings, PROD_FILE, DEBUG_FILE)

    # file is of type file found in flask
    # TODO: Needs a test.
    def upload_recipe_image(self, entity_id: int, file):
        recipe = self.get_entity(entity_id)
        file.save(self.get_image_filename(entity_id))
        recipe.has_image = True
        self._write_entities_to_file()

    # TODO: Needs a test.
    def modify_entity(self, entity_id: int, data: Dict[str, str]):
        EntityManager.modify_entity(self, entity_id, data)
        if data[Recipe.HAS_IMAGE_HEADER].lower() != 'true':
            image_filename = self.get_image_filename(entity_id)
            if os.path.exists(image_filename):
                os.remove(image_filename)

    def get_image_filename(self, entity_id):
        return "%sRecipeImages/%s.jpg" % (self._settings.recipe_app_directory, entity_id)
