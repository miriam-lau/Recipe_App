from .city import City
from .entity_manager import EntityManager
from src.settings.settings import Settings

PROD_FILE = "Recipe Database - cities.csv"
DEBUG_FILE = "Recipe Database - cities (copy).csv"


class CityManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, City, settings, PROD_FILE, DEBUG_FILE)

    def get_sorted_cities(self):
        return sorted(self._entity_map.values(), key=lambda entity: entity.name)
