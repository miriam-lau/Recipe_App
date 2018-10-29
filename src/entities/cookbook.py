from __future__ import annotations
from typing import Dict, List
from .entity import Entity
from .recipe import Recipe
from src.utils.utils import compare


SUCCESS_THRESHOLD = 7.0
PRIORITY_THRESHOLD = 1.0


class Cookbook(Entity):

    NOTES_HEADER = "notes"
    NAME_HEADER = "name"

    def __init__(self, entity_id, data: Dict[str, str]):
        Entity.__init__(self, entity_id, None)
        self.name: str = None
        self.notes: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent_unused, data) -> Cookbook:
        return Cookbook(entity_id, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: "0",
            Cookbook.NAME_HEADER: self.name,
            Cookbook.NOTES_HEADER: self.notes
        }

    def modify(self, data):
        if Cookbook.NAME_HEADER in data:
            self.name = data[Cookbook.NAME_HEADER]
        if Cookbook.NOTES_HEADER in data:
            self.notes = data[Cookbook.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, Cookbook.NAME_HEADER, Cookbook.NOTES_HEADER]

    @property
    def recipes(self):
        return self._children

    def recipes_by_best_rating_descending(self) -> List[Recipe]:
        return sorted(self.recipes, key=lambda recipe: recipe.get_best_rating(), reverse=True)

    def num_recipes_made(self):
        made = 0
        for recipe in self.recipes:
            if len(recipe.entries) > 0:
                made += 1
        return made

    def success_percentage(self) -> int:
        total = self.num_recipes_made()
        if total == 0:
            return 0
        success = 0
        for recipe in self.recipes:
            if compare(recipe.get_best_rating(), SUCCESS_THRESHOLD) >= 0:
                success += 1
        return round(success * 100 / total)

    def num_recipes_want_to_make(self):
        total = 0
        for recipe in self.recipes:
            if compare(recipe.priority, PRIORITY_THRESHOLD) >= 0:
                total += 1
        return total

    def __str__(self):
        return "entity id: %s, name: %s, notes: %s" % (self.entity_id, self.name, self.notes)

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.name == other.name and self.notes == other.notes
