from .entry import Entry
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from .recipe_manager import RecipeManager
from ..settings import settings
import datetime

ENTRIES_FILE_PREFIXES = ["/Users/miriamlau", "/home/james"]
DROPBOX_FILE = "/Dropbox/RecipeApp/"
PROD_ENTRIES_FILE_POSTFIX = "Recipe Database - entries.csv"
DEBUG_ENTRIES_FILE_POSTFIX = "Recipe Database - entries (copy).csv"


def _get_entry_file():
    entries_filename = ""
    entries_file_postfix = DEBUG_ENTRIES_FILE_POSTFIX if settings.get_debug_mode() else PROD_ENTRIES_FILE_POSTFIX
    for entries_file_prefix in ENTRIES_FILE_PREFIXES:
        entries_filename = entries_file_prefix + DROPBOX_FILE + entries_file_postfix
        cookbook_file = Path(entries_filename)
        if cookbook_file.is_file():
            return entries_filename
    return ""


class EntryManager:

    def __init__(self):
        self._entries = {}

    @staticmethod
    def create_and_initialize_entry_manager(recipe_manager: RecipeManager, filename: str=_get_entry_file()):
        entry_manager = EntryManager()
        with open(filename, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for entry_values in csv_reader:
                entry = Entry.from_values(entry_values)
                entry_manager.add_existing_entry(entry)
                recipe_manager.get_recipe(entry.recipe_id).add_entry(entry)
        return entry_manager

    # Adds entries that already have an id.
    def add_existing_entry(self, entry: Entry):
        assert entry.id is not None, "Entry id should not be None"
        self._entries[entry.id] = entry

    def add_new_entry(self, recipe_manager: RecipeManager, entry: Entry, filename: str=_get_entry_file()):
        assert entry.id is None, "Entry id should be None"
        entry_id = self._generate_entry_id()
        entry.id = entry_id
        self._entries[entry_id] = entry
        recipe_manager.get_recipe(entry.recipe_id).add_entry(entry)
        self._write_entries_to_file(filename)

    def modify_entry(self, id: int, date: datetime, miriam_rating: float, james_rating: float, \
                     miriam_comments: str, james_comments: str, filename: str=_get_entry_file()):
        entry = self.get_entry(id)
        entry.date = date
        entry.miriam_rating = miriam_rating
        entry.james_rating = james_rating
        entry.miriam_comments = miriam_comments
        entry.james_comments = james_comments
        self._write_entries_to_file(filename)

    def _write_entries_to_file(self, filename: str):
        with atomic_write(filename, keep=False) as f:
            writer = csv.writer(f, dialect=csv.excel)
            for entry in sorted(self._entries.values(), key=lambda entry: entry.id):
                writer.writerow(entry.to_tuple())

    def _generate_entry_id(self):
        i = 1
        while i in self._entries:
            i += 1
        return i

    def get_entries(self):
        return sorted(self._entries.values(), key=lambda entry: entry.id)

    def get_entry(self, id: int):
        return self._entries[id]
