from .entry import Entry
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from .recipe_manager import RecipeManager
from src.settings.settings import Settings
import datetime

PROD_FILE = "Recipe Database - entries.csv"
DEBUG_FILE = "Recipe Database - entries (copy).csv"


class EntryManager:

    def __init__(self, settings: Settings):
        self._entries = {}
        self._settings = settings

    def get_entries_file(self):
        file_prefix = self._settings.recipe_app_directory
        file_postfix = DEBUG_FILE if self._settings.debug_mode else PROD_FILE
        return file_prefix + file_postfix

    @staticmethod
    def create_and_initialize_entry_manager(recipe_manager, settings: Settings):
        entry_manager = EntryManager(settings)
        with open(entry_manager.get_entries_file(), 'rt') as csvfile:
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

    def add_new_entry(self, recipe_manager, recipe_id: str, date: str, miriam_rating: str, james_rating: str, \
                      miriam_comments: str, james_comments: str) -> Entry:
        entry_id = self._generate_entry_id()
        entry = Entry(entry_id, int(recipe_id), datetime.datetime.strptime(date, '%Y-%m-%d'), \
                      float(miriam_rating), float(james_rating), \
                      miriam_comments, james_comments)
        self._entries[entry_id] = entry
        recipe_manager.get_recipe(entry.recipe_id).add_entry(entry)
        self._write_entries_to_file()
        return entry

    def modify_entry(self, id: int, date: datetime, miriam_rating: float, james_rating: float, \
                     miriam_comments: str, james_comments: str):
        entry = self.get_entry(id)
        entry.date = date
        entry.miriam_rating = miriam_rating
        entry.james_rating = james_rating
        entry.miriam_comments = miriam_comments
        entry.james_comments = james_comments
        self._write_entries_to_file()

    def delete_entry(self, recipe_manager, id: int):
        entry = self.get_entry(id)
        recipe_manager.get_recipe(entry.recipe_id).remove_entry(entry)
        del self._entries[id]
        self._write_entries_to_file()

    def _write_entries_to_file(self):
        with atomic_write(self.get_entries_file(), keep=False) as f:
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
