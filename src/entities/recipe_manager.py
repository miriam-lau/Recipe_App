from .recipe import Recipe
from .entity_manager import EntityManager

from src.settings.settings import Settings

PROD_FILE  = "Recipe Database - recipes.csv"
DEBUG_FILE = "Recipe Database - recipes (copy).csv"


class RecipeManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Recipe, settings, PROD_FILE, DEBUG_FILE)

    def get_image_filename(self, entity_id):
        return "%sRecipeImages/%s.jpg" % (self._settings.recipe_app_directory, entity_id)
