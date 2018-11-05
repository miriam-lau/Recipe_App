from __future__ import annotations
from typing import Dict
from .entity import Entity


class Dish(Entity):
    NAME_HEADER = "name"
    PRIORITY_HEADER = "priority"
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
    def from_dict(entity_id, parent, data) -> Dish:
        return Dish(entity_id, parent, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: str(self.parent.entity_id),
            Dish.NAME_HEADER: self.name,
            Dish.PRIORITY_HEADER: str(self.priority),
            Entity.HAS_IMAGE_HEADER: str(self.has_image),
            Dish.CATEGORY_HEADER: self.category,
            Dish.NOTES_HEADER: self.notes
        }

    def modify(self, data: Dict[str, str]):
        if Dish.NAME_HEADER in data:
            self.name = data[Dish.NAME_HEADER]
        if Dish.PRIORITY_HEADER in data:
            self.priority = int(data[Dish.PRIORITY_HEADER])
        if Entity.HAS_IMAGE_HEADER in data:
            self.has_image = data[Entity.HAS_IMAGE_HEADER].lower() == "true"
        if Dish.CATEGORY_HEADER in data:
            self.category = data[Dish.CATEGORY_HEADER]
        if Dish.NOTES_HEADER in data:
            self.notes = data[Dish.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, Dish.NAME_HEADER, Dish.PRIORITY_HEADER, \
                Entity.HAS_IMAGE_HEADER, Dish.CATEGORY_HEADER, Dish.NOTES_HEADER]

    @property
    def dish_entries(self):
        return self._children

    def get_num_times_tried(self):
        return len(self.dish_entries)

    def get_best_rating(self):
        rating = 0.0
        for entry in self.dish_entries:
            entry_rating = entry.get_overall_rating()
            if entry_rating > rating:
                rating = entry_rating
        return rating

    def get_latest_rating(self):
        if len(self.dish_entries) == 0:
            return 0.0
        entities_by_date = self.dish_entries_by_date_descending()
        return entities_by_date[0].get_overall_rating()

    def dish_entries_by_date_descending(self):
        return sorted(self.dish_entries, key=lambda entry: entry.date, reverse=True)

    def __str__(self):
        return "id: %s, parent id: %s, name: %s, priority: %s, has_image: %s, category: %s, notes: %s" % \
               (self.entity_id, self.parent.entity_id, self.name, self.priority, self.has_image, self.category,
                self.notes)

    # For unit testing
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.parent == other.parent and self.name == other.name and \
               self.priority == other.priority and self.has_image == other.has_image and self.category == other.category

