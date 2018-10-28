import math
from typing import Tuple, Dict
import datetime
from .entity import Entity


class Entry(Entity):

    def __init__(self, entity_id: int, recipe_id: int, date: datetime, miriam_rating: float, james_rating: float, \
                 miriam_comments, james_comments):
        Entity.__init__(self, entity_id, recipe_id)
        self.date: datetime = date
        self.miriam_rating: float = miriam_rating
        self.james_rating: float = james_rating
        self.miriam_comments: str = miriam_comments
        self.james_comments: str = james_comments

    @staticmethod
    def from_tuple(entity_id: int, parent_id: int, values: Tuple[str]):
        return Entry(entity_id, parent_id, datetime.datetime.strptime(values[0], "%Y-%m-%d"), \
                     float(values[1]), float(values[2]), values[3], values[4])

    def to_tuple(self):
        return self.entity_id, self.recipe_id, self.date.strftime("%Y-%m-%d"), self.miriam_rating, self.james_rating, \
               self.miriam_comments, self.james_comments

    def modify(self, values: Dict[str, str]):
        self.date = datetime.datetime.strptime(values["date"], '%Y-%m-%d')
        self.miriam_rating = float(values["miriam_rating"])
        self.james_rating = float(values["james_rating"])
        self.miriam_comments = values["miriam_comments"]
        self.james_comments = values["james_comments"]

    @property
    def recipe_id(self):
        return self._parent_id

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
        return self.entity_id == other.entity_id and self.recipe_id == other.recipe_id and self.date == other.date and \
            math.isclose(self.miriam_rating, other.miriam_rating) and \
               math.isclose(self.james_rating, other.james_rating) and \
               self.miriam_comments == other.miriam_comments and self.james_comments == other.james_comments

    def __str__(self):
        return "id: %s, parent id: %s, date: %s, miriam_rating: %s, james_rating: %s, miriam_comments: %s, \
        james_comments: %s" % (self.id, self.parent_id, self.date, self.miriam_rating, self.james_rating, \
                               self.miriam_comments, self.james_comments)
