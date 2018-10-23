import math


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
        return self._miriam_rating

    @miriam_rating.setter
    def miriam_rating(self, miriam_rating):
        self._miriam_rating = miriam_rating

    @property
    def james_rating(self):
        return self._james_rating

    @james_rating.setter
    def james_rating(self, james_rating):
        self._james_rating = james_rating

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
    def from_line(line: str):
        line = line.strip("\n")
        split_line = line.split(",")
        return Entry(int(split_line[0]), int(split_line[1]), split_line[2], float(split_line[3]), \
                     float(split_line[4]), split_line[5], split_line[6])

    def to_line(self):
        return "%i,%i,%s,%.1f,%.1f,%s,%s\n" % (self._id, self._recipe_id, self._date, self._miriam_rating, \
                                               self._james_rating, self._miriam_comments, self._james_comments)

    def __eq__(self, other):
        return self.id == other.id and self.recipe_id == other.recipe_id and self.date == other.date and \
            math.isclose(self.miriam_rating, other.miriam_rating) and \
               math.isclose(self.james_rating, other.james_rating) and \
               self.miriam_comments == other.miriam_comments and self.james_comments == other.james_comments
