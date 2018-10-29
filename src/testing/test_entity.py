from typing import Dict, List
from src.entities.entity import Entity


class TestEntity(Entity):

    NOTES_HEADER = "notes"
    NAME_HEADER = "name"

    def __init__(self, entity_id, parent, data: Dict[str, str]):
        Entity.__init__(self, entity_id, parent)
        self.name: str = None
        self.notes: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent, data):
        return TestEntity(entity_id, parent, data)

    def to_dict(self):
        parent_id = self.parent_id
        parent_id_str = "0"
        if parent_id:
            parent_id_str = str(parent_id)
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: parent_id_str,
            TestEntity.NAME_HEADER: self.name,
            TestEntity.NOTES_HEADER: self.notes
        }

    def modify(self, data):
        self.name = data[TestEntity.NAME_HEADER]
        self.notes = data[TestEntity.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, TestEntity.NAME_HEADER, TestEntity.NOTES_HEADER]

    def __str__(self):
        return "entity id: %s, parent: {%s}, name: %s, notes: %s" % (
            self.entity_id, str(self.parent), self.name, self.notes)

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.parent == other.parent and \
               self.name == other.name and self.notes == other.notes
