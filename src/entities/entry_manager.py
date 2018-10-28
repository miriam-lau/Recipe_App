from .entry import Entry
from .entity_manager import EntityManager
from src.settings.settings import Settings

PROD_FILE = "Recipe Database - entries.csv"
DEBUG_FILE = "Recipe Database - entries (copy).csv"


class EntryManager(EntityManager):

    def __init__(self, settings: Settings):
        EntityManager.__init__(self, Entry, settings, PROD_FILE, DEBUG_FILE)
