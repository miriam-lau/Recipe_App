from typing import Tuple, Dict, Optional


class Entity:
    def __init__(self, entity_id: int, parent_id: Optional[int]):
        self._entity_id = entity_id
        self._children = []
        self._parent_id = parent_id

    @property
    def entity_id(self):
        return self._entity_id

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

    # For generating an entity by parsing the input csv file.
    @staticmethod
    def from_tuple(entity_id: int, parent_id: int, values: Tuple[str]):
        pass

    def to_tuple(self):
        pass

    def modify(self, values: Dict[str, str]):
        pass
