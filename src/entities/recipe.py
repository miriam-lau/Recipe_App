class Recipe:

    def __init__(self, id: int, cookbook_id: int, name: str, priority: int, image: str, category: str):
        self._id: int = id
        self._cookbook_id: int = cookbook_id
        self._name: str = name
        self._priority: int = priority
        self._image: str = image
        self._category: str = category

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
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    # Generates a recipe from a text string that represents it.
    @staticmethod
    def from_line(line: str):
        line = line.strip("\n")
        split_line = line.split(",")
        return Recipe(int(split_line[0]), int(split_line[1]), split_line[2], int(split_line[3]), split_line[4], \
                      split_line[5])

    def to_line(self):
        return "%i,%i,%s,%i,%s,%s\n" % (self._id, self._cookbook_id, self._name, self._priority, self._image, \
                                        self._category)

    def __eq__(self, other):
        return self.id == other.id and self.cookbook_id == other.cookbook_id and self.name == other.name and \
               self.priority == other.priority and self.image == other.image and self.category == other.category
