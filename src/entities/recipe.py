class Recipe:

    def __init__(self, id: int, cookbook_id: int, name: str, priority: int, has_image: bool, category: str, notes: str):
        self._id: int = id
        self._cookbook_id: int = cookbook_id
        self._name: str = name
        self._priority: int = priority
        self._has_image: bool = has_image
        self._category: str = category
        self._notes: str = notes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def cookbook_id(self):
        return self._cookbook_id

    @cookbook_id.setter
    def cookbook_id(self, cookbook_id):
        self._cookbook_id = cookbook_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    @property
    def has_image(self):
        return self._has_image

    @has_image.setter
    def has_image(self, has_image):
        self._has_image = has_image

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    # Generates a recipe from a text string that represents it.
    @staticmethod
    def from_line(line: str):
        line = line.strip("\n")
        split_line = line.split(",")
        return Recipe(int(split_line[0]), int(split_line[1]), split_line[2], int(split_line[3]), bool(split_line[4]), \
                      split_line[5], split_line[6])

    def to_line(self):
        return "%i,%i,%s,%i,%s,%s,%s\n" % (self._id, self._cookbook_id, self._name, self._priority, self._has_image, \
                                           self._category, self._notes)

    def __eq__(self, other):
        return self.id == other.id and self.cookbook_id == other.cookbook_id and self.name == other.name and \
               self.priority == other.priority and self.has_image == other.has_image and self.category == other.category
