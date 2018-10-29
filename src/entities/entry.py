from __future__ import annotations
import math
from typing import Dict
import datetime
from .entity import Entity


class Entry(Entity):

    DATE_HEADER = "date"
    MIRIAM_RATING_HEADER = "miriam rating"
    JAMES_RATING_HEADER = "james rating"
    MIRIAM_COMMENTS_HEADER = "miriam comments"
    JAMES_COMMENTS_HEADER = "james comments"

    def __init__(self, entity_id, parent, data: Dict[str, str]):
        Entity.__init__(self, entity_id, parent)
        self.date: datetime = None
        self.miriam_rating: float = None
        self.james_rating: float = None
        self.miriam_comments: str = None
        self.james_comments: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent, data) -> Entry:
        return Entry(entity_id, parent, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: str(self.parent.entity_id),
            Entry.DATE_HEADER: self.date_string(),
            Entry.MIRIAM_RATING_HEADER: str(self.miriam_rating),
            Entry.JAMES_RATING_HEADER: str(self.james_rating),
            Entry.MIRIAM_COMMENTS_HEADER: self.miriam_comments,
            Entry.JAMES_COMMENTS_HEADER: self.james_comments
        }

    def modify(self, data):
        if Entry.DATE_HEADER in data:
            self.date = datetime.datetime.strptime(data[Entry.DATE_HEADER], '%Y-%m-%d')
        if Entry.MIRIAM_RATING_HEADER in data:
            self.miriam_rating = float(data[Entry.MIRIAM_RATING_HEADER])
        if Entry.JAMES_RATING_HEADER in data:
            self.james_rating = float(data[Entry.JAMES_RATING_HEADER])
        if Entry.MIRIAM_COMMENTS_HEADER in data:
            self.miriam_comments = data[Entry.MIRIAM_COMMENTS_HEADER]
        if Entry.JAMES_COMMENTS_HEADER in data:
            self.james_comments = data[Entry.JAMES_COMMENTS_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, Entry.DATE_HEADER, Entry.MIRIAM_RATING_HEADER,
                Entry.JAMES_RATING_HEADER, Entry.MIRIAM_COMMENTS_HEADER, Entry.JAMES_COMMENTS_HEADER]

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

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.parent == other.parent and self.date == other.date and \
            math.isclose(self.miriam_rating, other.miriam_rating) and \
            math.isclose(self.james_rating, other.james_rating) and \
            self.miriam_comments == other.miriam_comments and self.james_comments == other.james_comments

    def __str__(self):
        return "id: %s, parent id: %s, date: %s, miriam_rating: %s, james_rating: %s, miriam_comments: %s, \
        james_comments: %s" % (self.id, self.parent.entity_id, self.date, self.miriam_rating, self.james_rating,
                               self.miriam_comments, self.james_comments)
