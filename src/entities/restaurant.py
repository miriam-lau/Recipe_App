from __future__ import annotations
from typing import Dict, List
from .entity import Entity
from .recipe import Recipe
from src.utils.utils import compare


class Restaurant(Entity):

    NAME_HEADER = "name"
    ADDRESS_HEADER = "address"
    CATEGORY_HEADER = "category"
    NOTES_HEADER = "notes"

    def __init__(self, entity_id, parent, data: Dict[str, str]):
        Entity.__init__(self, entity_id, parent)
        self.name: str = None
        self.category: str = None
        self.address: str = None
        self.notes: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent, data) -> Restaurant:
        return Restaurant(entity_id, parent, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: str(self.parent.entity_id),
            Restaurant.NAME_HEADER: self.name,
            Restaurant.ADDRESS_HEADER: self.address,
            Restaurant.CATEGORY_HEADER: self.category,
            Restaurant.NOTES_HEADER: self.notes
        }

    def modify(self, data):
        if Restaurant.NAME_HEADER in data:
            self.name = data[Restaurant.NAME_HEADER]
        if Restaurant.ADDRESS_HEADER in data:
            self.address = data[Restaurant.ADDRESS_HEADER]
        if Restaurant.CATEGORY_HEADER in data:
            self.category = data[Restaurant.CATEGORY_HEADER]
        if Restaurant.NOTES_HEADER in data:
            self.notes = data[Restaurant.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, Restaurant.NAME_HEADER, Restaurant.CATEGORY_HEADER,
                Restaurant.ADDRESS_HEADER, Restaurant.NOTES_HEADER]

    @property
    def dishes(self):
        return self._children

    def dishes_by_best_rating_descending(self) -> List[Recipe]:
        return sorted(self.dishes, key=lambda dish: dish.get_best_rating(), reverse=True)

    def get_num_dishes_tried(self):
        made = 0
        for dish in self.dishes:
            if len(dish.dish_entries) > 0:
                made += 1
        return made

    def get_best_rating(self) -> float:
        rating = 0.0
        for dish in self.dishes:
            dish_rating = dish.get_best_rating()
            if dish_rating > rating:
                rating = dish_rating
        return rating

    def __str__(self):
        return "entity id: %s, name: %s, address: %s, category: %s, notes: %s" % (
            self.entity_id, self.name, self.address, self.category, self.notes)

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.name == other.name and self.address == other.address and \
               self.category == other.category and self.notes == other.notes
