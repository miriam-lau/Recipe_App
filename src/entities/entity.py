class Entity:
    def __init__(self, id, parent_id):
        self._id = id
        self._children = []
        self._parent_id = parent_id

    @property
    def id(self):
        return self._id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)

