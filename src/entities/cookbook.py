from typing import List
from entities.recipe import Recipe


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

    # Generates a cookbook from a text string that represents it.
    @staticmethod
    def from_values(values: List[str]):
        return Cookbook(int(values[0]), values[1], values[2])

    def to_tuple(self):
        return self._id, self._name, self._notes

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.notes == other.notes
