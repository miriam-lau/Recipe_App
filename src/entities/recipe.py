from typing import List
from entities.entry import Entry

# TODO: There's a bug where has image is true but it should be false.
class Recipe:

    def __init__(self, id: int, cookbook_id: int, name: str, priority: int, has_image: bool, category: str, notes: str):
        self._id: int = id
        self._cookbook_id: int = cookbook_id
        self._name: str = name
        self._priority: int = priority
        self._has_image: bool = has_image
        self._category: str = category
        self._notes: str = notes
        self._entries: List[Entry] = []

    def add_entry(self, entry: Entry):
        self._entries.append(entry)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def cookbook_id(self):
        return self._cookbook_id

    @cookbook_id.setter
    def cookbook_id(self, cookbook_id):
        self._cookbook_id = cookbook_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    @property
    def has_image(self):
        return self._has_image

    @has_image.setter
    def has_image(self, has_image):
        self._has_image = has_image

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @property
    def entries(self):
        return self._entries

    # Generates a recipe from a text string that represents it.
    @staticmethod
    def from_values(values: List[str]):
        return Recipe(int(values[0]), int(values[1]), values[2], int(values[3]), bool(values[4]), \
                      values[5], values[6])

    def to_tuple(self):
        return self._id, self._cookbook_id, self._name, self._priority, self._has_image, self._category, self._notes

    def __eq__(self, other):
        return self.id == other.id and self.cookbook_id == other.cookbook_id and self.name == other.name and \
               self.priority == other.priority and self.has_image == other.has_image and self.category == other.category

    def get_best_rating(self):
        rating = 0.0
        for entry in self.entries:
            entry_rating = entry.get_overall_rating()
            if (entry_rating > rating):
                rating = entry_rating
        return rating

    def get_num_times_made(self):
        return len(self.entries)