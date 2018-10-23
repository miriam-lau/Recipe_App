from entities.entry import Entry

ENTRIES_FILE = "/home/james/Dropbox/RecipeApp/entries.txt"


class EntryManager:

    def __init__(self):
        self._entries = {}

    @staticmethod
    def create_and_initialize_entry_manager(filename: str=ENTRIES_FILE):
        entry_manager = EntryManager()
        entry_file = open(filename, "r")
        for entry_line in entry_file:
            if entry_line.strip("\n"):
                entry = Entry.from_line(entry_line)
                entry_manager.add_existing_entry(entry)
        entry_file.close()
        return entry_manager

    # Adds entries that already have an id.
    def add_existing_entry(self, entry: Entry):
        assert entry.id is not None, "Entry id should not be None"
        self._entries[entry.id] = entry

    def add_new_entry(self, entry: Entry, filename: str=ENTRIES_FILE):
        assert entry.id is None, "Entry id should be None"
        entry_id = self._generate_entry_id()
        entry.id = entry_id
        self._entries[entry_id] = entry
        self._write_entries_to_file(filename)

    def _write_entries_to_file(self, filename: str):
        with open(filename, "w") as f:
            for entry in sorted(self._entries.values(), key=lambda entry: entry.id):
                f.write(entry.to_line())
            f.write("\n")

    def _generate_entry_id(self):
        i = 1
        while i in self._entries:
            i += 1
        return i

    def get_entries(self):
        return sorted(self._entries.values(), key=lambda entry: entry.id)

    # TODO: Make entries sorted by date.
    def get_entries_for_recipe(self, id: int):
        entries = self._entries.values()
        entries = filter(lambda entry: entry.recipe_id == id, entries)
        return sorted(entries, key=lambda entry: entry.id)
