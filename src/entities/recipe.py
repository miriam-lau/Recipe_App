from typing import Tuple, Dict
import datetime
from .entity import Entity


# TODO: There's a bug where has image is true but it should be false.
class Recipe(Entity):

    def __init__(self, entity_id: int, cookbook_id: int, name: str, priority: int, has_image: bool, category: str, notes: str):
        Entity.__init__(self, entity_id, cookbook_id)
        self.name: str = name
        self.priority: int = priority
        self.has_image: bool = has_image
        self.category: str = category
        self.notes: str = notes

    @staticmethod
    def from_tuple(id: int, parent_id: int, values: Tuple[str]):
        return Recipe(id, parent_id, values[0], int(values[1]), values[2].lower() == "true", \
                      values[3], values[4])

    def to_tuple(self):
        return self.entity_id, self.cookbook_id, self.name, self.priority, self.has_image, self.category, self.notes

    def modify(self, values: Dict[str, str]):
        self.name = values["name"]
        self.priority = int(values["priority"])
        self.has_image = values["has_image"].lower() == "true"
        self.category = values["category"]
        self.notes = values["notes"]

    @property
    def cookbook_id(self):
        return self._parent_id

    @property
    def entries(self):
        return self._children

    # For unit testing
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.cookbook_id == other.cookbook_id and self.name == other.name and \
               self.priority == other.priority and self.has_image == other.has_image and self.category == other.category

    def get_best_rating(self):
        rating = 0.0
        for entry in self.entries:
            entry_rating = entry.get_overall_rating()
            if entry_rating > rating:
                rating = entry_rating
        return rating

    def entries_by_date_descending(self):
        return sorted(self.entries, key=lambda entry: entry.date, reverse=True)

    def get_latest_rating(self):
        if len(self.entries) == 0:
            return 0.0
        entities_by_date = self.entries_by_date_descending()
        return entities_by_date[0].get_overall_rating()

    def get_num_times_made(self):
        return len(self.entries)

    # Hack: Should not be here. Only here so that recipe.html can use it. Can probably call it directly from there.
    def get_today_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def get_image_filename(self, settings):
        return "%sRecipeImages/%s.jpg" % (settings.recipe_app_directory, self.entity_id)

    def __str__(self):
        return "id: %s, parent id: %s, name: %s, priority: %s, has_image: %s, category: %s, notes: %s" % \
               (self.entity_id, self.parent_id, self.name, self.priority, self.has_image, self.category, self.notes)
