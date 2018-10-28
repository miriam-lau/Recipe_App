import csv
from typing import Tuple
from .files.files import write_entities_to_file
from .entity import Entity


class EntityManager:

    # entity_class needs a type.
    def __init__(self, entity_class, settings, prod_file: str, debug_file: str):
        self._entity_map = {}
        self._entity_class = entity_class
        self._settings = settings
        self._prod_file = prod_file
        self._debug_file = debug_file
        self.parent_entity_manager = None
        self.children_entity_manager = None

    def get_entities_file(self):
        file_prefix = self._settings.recipe_app_directory
        file_postfix = self._debug_file if self._settings.debug_mode else self._prod_file
        return file_prefix + file_postfix

    def initialize(self):
        with open(self.get_entities_file(), 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, dialect=csv.excel)
            for entity_values in csv_reader:
                entity = self._entity_class.from_tuple(int(entity_values[0]), int(entity_values[1]), entity_values[2:])
                self.add_existing_entity(entity)

    # Adds entities that already have an id.
    def add_existing_entity(self, entity):
        assert entity.id is not None, "Entity id should not be None"
        self._entity_map[entity.id] = entity
        if self.parent_entity_manager:
            self.parent_entity_manager.get_entity(entity.parent_id).add_child(entity)

    def add_new_entity(self, parent_id: int, values: Tuple[str]) -> Entity:
        entity_id = self._generate_entity_id()
        entity = self._entity_class.from_tuple(entity_id, parent_id, values)
        self._entity_map[entity_id] = entity
        if self.parent_entity_manager:
            self.parent_entity_manager.get_entity(parent_id).add_child(entity)
        self.write_entities_to_file()
        return entity

    def modify_entity(self, id: int, values: Tuple[str]):
        entity = self.get_entity(id)
        entity.modify(values)
        self.write_entities_to_file()

    def delete_entity(self, id: int):
        entity = self.get_entity(id)
        if self.children_entity_manager:
            entity_children = []
            for child in entity.children:
                entity_children.append(child)
            for child in entity_children:
                self.children_entity_manager.delete_entity(child.id)
        if self.parent_entity_manager:
            self.parent_entity_manager.get_entity(entity.parent_id).remove_child(entity)
        del self._entity_map[id]
        self.write_entities_to_file()

    def write_entities_to_file(self):
        write_entities_to_file(self.get_entities_file(), self._entity_map.values())

    def _generate_entity_id(self):
        i = 1
        while i in self._entity_map:
            i += 1
        return i

    def _get_entities(self):
        return sorted(self._entity_map.values(), key=lambda entity: entity.name.lower())

    def get_entity(self, id: int):
        return self._entity_map[id]
