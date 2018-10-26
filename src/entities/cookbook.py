from typing import List
from .recipe import Recipe


SUCCESS_THRESHOLD = 6.99
PRIORITY_THRESHOLD = 0.99


class Cookbook:

    def __init__(self, id: int, name: str, notes: str):
        self._id: int = id
        self.name: str = name
        self.notes: str = notes
        self._recipes: List[Recipe] = []

    def add_recipe(self, recipe: Recipe):
        self._recipes.append(recipe)

    def remove_recipe(self, recipe: Recipe):
        self._recipes.remove(recipe)

    @property
    def id(self):
        return self._id

    @property
    def recipes(self):
        return self._recipes

    def recipes_by_best_rating_descending(self):
        return sorted(self.recipes, key=lambda recipe: recipe.get_best_rating(), reverse=True)

    # Generates a cookbook from a text string that represents it.
    @staticmethod
    def from_values(values: List[str]):
        return Cookbook(int(values[0]), values[1], values[2])

    def to_tuple(self):
        return self._id, self.name, self.notes

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
