class Cookbook:

    def __init__(self, id: int, name: str, notes: str):
        self._id: int = id
        self._name: str = name
        self._notes: str = notes

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

    # Generates a cookbook from a text string that represents it.
    @staticmethod
    def from_line(line: str):
        line = line.strip("\n")
        split_line = line.split(",")
        return Cookbook(int(split_line[0]), split_line[1], split_line[2])

    def to_line(self):
        return "%i,%s,%s\n" % (self._id, self._name, self._notes)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.notes == other.notes
