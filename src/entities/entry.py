import math
from typing import List
import datetime


class Entry:

    def __init__(self, id: int, recipe_id: int, date: datetime, miriam_rating: float, james_rating: float, \
                 miriam_comments: str, james_comments: str):
        self._id: int = id
        self._recipe_id: int = recipe_id
        self.date: str = date
        self.miriam_rating: float = miriam_rating
        self.james_rating: float = james_rating
        self.miriam_comments: str = miriam_comments
        self.james_comments: str = james_comments

    @property
    def id(self):
        return self._id

    @property
    def recipe_id(self):
        return self._recipe_id

    # Generates an entry from a text string that represents it.
    @staticmethod
    def from_values(values: List[str]):
        return Entry(int(values[0]), int(values[1]), datetime.datetime.strptime(values[2], '%Y-%m-%d'), \
                     float(values[3]), float(values[4]), values[5], values[6])

    def to_tuple(self):
        return self.id, self.recipe_id, self.date.strftime("%Y-%m-%d"), self.miriam_rating, self.james_rating, \
               self.miriam_comments, self.james_comments

    def date_string(self):
        return self.date.strftime("%Y-%m-%d")

    def get_overall_rating(self):
        rating = 0.0
        if (not math.isclose(self.miriam_rating, 0)) and (not math.isclose(self.james_rating, 0)):
            rating = (self.miriam_rating + self.james_rating) / 2
        elif math.isclose(self.miriam_rating, 0):
            rating = self.james_rating
        elif math.isclose(self.james_rating, 0):
            rating = self.miriam_rating
        return round(rating, 1)

    def __eq__(self, other):
        return self.id == other.id and self.recipe_id == other.recipe_id and self.date == other.date and \
            math.isclose(self.miriam_rating, other.miriam_rating) and \
               math.isclose(self.james_rating, other.james_rating) and \
               self.miriam_comments == other.miriam_comments and self.james_comments == other.james_comments
