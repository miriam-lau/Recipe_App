from .cookbook import Cookbook
from .entity_manager import EntityManager
from src.settings.settings import Settings

PROD_FILE = "Recipe Database - cookbooks.csv"
DEBUG_FILE = "Recipe Database - cookbooks (copy).csv"


class CookbookManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Cookbook, settings, PROD_FILE, DEBUG_FILE)

    def get_cookbooks(self):
        return self._get_entities()

    def get_cookbook(self, entity_id: int):
        return self.get_entity(entity_id)
