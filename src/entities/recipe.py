from __future__ import annotations
from typing import Dict
from .entity import Entity


# TODO: There's a bug where has image is true but it should be false.
class Recipe(Entity):
    NAME_HEADER = "name"
    PRIORITY_HEADER = "priority"
    HAS_IMAGE_HEADER = "has image"
    CATEGORY_HEADER = "category"
    NOTES_HEADER = "notes"

    def __init__(self, entity_id, parent, data: Dict[str, str]):
        Entity.__init__(self, entity_id, parent)
        self.name: str = None
        self.priority: int = None
        self.has_image: bool = None
        self.category: str = None
        self.notes: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent, data) -> Recipe:
        return Recipe(entity_id, parent, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: str(self.parent.entity_id),
            Recipe.NAME_HEADER: self.name,
            Recipe.PRIORITY_HEADER: str(self.priority),
            Recipe.HAS_IMAGE_HEADER: str(self.has_image),
            Recipe.CATEGORY_HEADER: self.category,
            Recipe.NOTES_HEADER: self.notes
        }

    def modify(self, data: Dict[str, str]):
        if Recipe.NAME_HEADER in data:
            self.name = data[Recipe.NAME_HEADER]
        if Recipe.PRIORITY_HEADER in data:
            self.priority = int(data[Recipe.PRIORITY_HEADER])
        if Recipe.HAS_IMAGE_HEADER in data:
            self.has_image = data[Recipe.HAS_IMAGE_HEADER].lower() == "true"
        if Recipe.CATEGORY_HEADER in data:
            self.category = data[Recipe.CATEGORY_HEADER]
        if Recipe.NOTES_HEADER in data:
            self.notes = data[Recipe.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, Recipe.NAME_HEADER, Recipe.PRIORITY_HEADER, \
                Recipe.HAS_IMAGE_HEADER, Recipe.CATEGORY_HEADER, Recipe.NOTES_HEADER]

    @property
    def entries(self):
        return self._children

    def get_num_times_made(self):
        return len(self.entries)

    def get_best_rating(self):
        rating = 0.0
        for entry in self.entries:
            entry_rating = entry.get_overall_rating()
            if entry_rating > rating:
                rating = entry_rating
        return rating

    def get_latest_rating(self):
        if len(self.entries) == 0:
            return 0.0
        entities_by_date = self.entries_by_date_descending()
        return entities_by_date[0].get_overall_rating()

    def entries_by_date_descending(self):
        return sorted(self.entries, key=lambda entry: entry.date, reverse=True)

    def __str__(self):
        return "id: %s, parent id: %s, name: %s, priority: %s, has_image: %s, category: %s, notes: %s" % \
               (self.entity_id, self.parent.entity_id, self.name, self.priority, self.has_image, self.category,
                self.notes)

    # For unit testing
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.parent == other.parent and self.name == other.name and \
               self.priority == other.priority and self.has_image == other.has_image and self.category == other.category

