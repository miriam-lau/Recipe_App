from typing import Tuple
from .entity import Entity


SUCCESS_THRESHOLD = 6.99
PRIORITY_THRESHOLD = 0.99


class Cookbook(Entity):

    def __init__(self, id: int, name, notes):
        Entity.__init__(self, id, None)
        self.name: str = name
        self.notes: str = notes

    @property
    def recipes(self):
        return self._children

    def recipes_by_best_rating_descending(self):
        return sorted(self.recipes, key=lambda recipe: recipe.get_best_rating(), reverse=True)

    # Generates a cookbook from a text string that represents it.
    @staticmethod
    def from_tuple(id: int, parent_id_unused, values: Tuple[str]):
        return Cookbook(id, values[0], values[1])

    def to_tuple(self):
        return self.id, "0", self.name, self.notes

    def modify(self, values: Tuple[str]):
        self.name = values[0]
        self.notes = values[1]

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.notes == other.notes

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
        return "id: %s, parent id: %s, name: %s, notes: %s" % (self.id, self.parent_id, self.name, self.notes)
