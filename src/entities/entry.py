import math
from typing import List


class Entry:

    def __init__(self, id: int, recipe_id: int, date: str, miriam_rating: float, james_rating: float, \
                 miriam_comments: str, james_comments: str):
        self._id: int = id
        self._recipe_id: int = recipe_id
        self._date: str = date
        self._miriam_rating: float = miriam_rating
        self._james_rating: float = james_rating
        self._miriam_comments: str = miriam_comments
        self._james_comments: str = james_comments

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def recipe_id(self):
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, recipe_id):
        self._recipe_id = recipe_id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def miriam_rating(self):
        return round(self._miriam_rating, 1)

    @miriam_rating.setter
    def miriam_rating(self, miriam_rating):
        self._miriam_rating = round(miriam_rating, 1)

    @property
    def james_rating(self):
        return round(self._james_rating, 1)

    @james_rating.setter
    def james_rating(self, james_rating):
        self._james_rating = round(james_rating, 1)

    @property
    def james_comments(self):
        return self._james_comments

    @james_comments.setter
    def james_comments(self, james_comments):
        self._james_comments = james_comments

    @property
    def miriam_comments(self):
        return self._miriam_comments

    @miriam_comments.setter
    def miriam_comments(self, miriam_comments):
        self._miriam_comments = miriam_comments

    # Generates an entry from a text string that represents it.
    @staticmethod
    def from_values(values: List[str]):
        return Entry(int(values[0]), int(values[1]), values[2], float(values[3]), \
                     float(values[4]), values[5], values[6])

    def to_tuple(self):
        return self._id, self._recipe_id, self._date, self._miriam_rating, self._james_rating, self._miriam_comments, \
               self._james_comments

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
