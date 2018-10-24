from typing import List
from entities.recipe import Recipe


SUCCESS_THRESHOLD = 6.99
PRIORITY_THRESHOLD = 0.99

class Cookbook:

    def __init__(self, id: int, name: str, notes: str):
        self._id: int = id
        self._name: str = name
        self._notes: str = notes
        self._recipes: List[Recipe] = []

    def add_recipe(self, recipe: Recipe):
        self._recipes.append(recipe)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

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
        return self._id, self._name, self._notes

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
