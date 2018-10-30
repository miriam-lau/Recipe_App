from .restaurant import Restaurant
from .entity_manager import EntityManager
from src.settings.settings import Settings

PROD_FILE = "Recipe Database - restaurants.csv"
DEBUG_FILE = "Recipe Database - restaurants (copy).csv"


class RestaurantManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Restaurant, settings, PROD_FILE, DEBUG_FILE)
