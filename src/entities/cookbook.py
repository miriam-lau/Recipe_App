from typing import Tuple, Dict, List
from .entity import Entity
from .recipe import Recipe


SUCCESS_THRESHOLD = 6.99
PRIORITY_THRESHOLD = 0.99


class Cookbook(Entity):

    def __init__(self, entity_id: int, name, notes):
        Entity.__init__(self, entity_id, None)
        self.name = name
        self.notes = notes

    @staticmethod
    def from_tuple(entity_id: int, parent_id_unused, values: Tuple[str]):
        return Cookbook(entity_id, values[0], values[1])

    def to_tuple(self):
        return self.entity_id, "0", self.name, self.notes

    def modify(self, values: Dict[str, str]):
        self.name = values["name"]
        self.notes = values["notes"]

    @property
    def recipes(self):
        return self._children

    def recipes_by_best_rating_descending(self) -> List[Recipe]:
        return sorted(self.recipes, key=lambda recipe: recipe.get_best_rating(), reverse=True)

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.name == other.name and self.notes == other.notes

    def num_recipes_made(self):
        made = 0
        for recipe in self.recipes:
            if len(recipe.entries) > 0:
                made += 1
        return made

    def success_percentage(self):
        total = self.num_recipes_made()
        if total == 0:
            return 0
        success = 0
        for recipe in self.recipes:
            if recipe.get_best_rating() >= SUCCESS_THRESHOLD:
                success += 1
        return round(success * 100 / total)

    def num_recipes_want_to_make(self):
        total = 0
        for recipe in self.recipes:
            if recipe.priority >= PRIORITY_THRESHOLD:
                total += 1
        return total

    def __str__(self):
        return "entity id: %s, parent id: %s, name: %s, notes: %s" % (self.entity_id, self.parent_id, self.name, self.notes)
