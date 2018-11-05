from __future__ import annotations
from typing import List, Dict, Optional


class Entity:

    ENTITY_ID_HEADER = "entity id"
    PARENT_ID_HEADER = "parent id"
    HAS_IMAGE_HEADER = "has image"

    def __init__(self, entity_id, parent: Optional[Entity]):
        self._entity_id: int = entity_id
        self._parent: Optional[Entity] = parent
        if parent:
            parent.add_child(self)
        self._children: List[Entity] = []

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def parent(self):
        return self._parent

    @property
    def parent_id(self) -> Optional[int]:
        if not self.parent:
            return None
        return self.parent.entity_id

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)

    @staticmethod
    def from_dict(entity_id, parent, data: Dict[str, str]) -> Entity:
        pass

    def to_dict(self) -> Dict[str, str]:
        pass

    def modify(self, values: Dict[str, str]):
        pass

    @staticmethod
    def file_headers() -> List[str]:
        pass
