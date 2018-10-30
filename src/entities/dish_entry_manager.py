from .dish_entry import DishEntry
from .entity_manager import EntityManager
from src.settings.settings import Settings

PROD_FILE = "Recipe Database - dish entries.csv"
DEBUG_FILE = "Recipe Database - dish entries (copy).csv"


class DishEntryManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, DishEntry, settings, PROD_FILE, DEBUG_FILE)
