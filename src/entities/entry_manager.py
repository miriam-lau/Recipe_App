from .entry import Entry
from pathlib import Path
import csv
from .files.atomic_write import atomic_write
from .recipe_manager import RecipeManager

ENTRY_FILES = ["/Users/miriamlau/Dropbox/RecipeApp/entries.csv", "/home/james/Dropbox/RecipeApp/entries.csv"]


def _get_entry_file():
    for entry_filename in ENTRY_FILES:
        entry_file = Path(entry_filename)
        if entry_file.is_file():
            return entry_filename
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
