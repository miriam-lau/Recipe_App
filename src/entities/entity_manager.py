import csv
from typing import Dict, Type, Optional
from .entity import Entity
from .files.files import atomic_write


class EntityManager:

    def __init__(self, entity_class: Type[Entity], settings, prod_filename, debug_filename):
        self._entity_map: Dict[int, Entity] = {}
        self._entity_class = entity_class
        self._settings = settings
        self._prod_filename = prod_filename
        self._debug_filename = debug_filename
        self.parent_entity_manager = None
        self.children_entity_manager = None

    @property
    def entity_class(self):
        return self._entity_class

    def get_entities_file(self):
        file_prefix = self._settings.recipe_app_directory
        file_postfix = self._debug_filename if self._settings.debug_mode else self._prod_filename
        return file_prefix + file_postfix

    # Both the parent and children entity managers must be set before initialize is called.
    def initialize(self):
        with open(self.get_entities_file(), 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, dialect=csv.excel)
            header_line = True
            header_map = {}
            for entity_values in csv_reader:
                if header_line:
                    header_line = False
                    for i in range(len(entity_values)):
                        header_map[i] = entity_values[i]
                else:
                    data = {}
                    for i in range(len(entity_values)):
                        data[header_map[i]] = entity_values[i]
                    entity_id_str = data[Entity.ENTITY_ID_HEADER]
                    parent_id_str = data[Entity.PARENT_ID_HEADER]
                    del data[Entity.ENTITY_ID_HEADER]
                    del data[Entity.PARENT_ID_HEADER]
                    parent = None
                    if self.parent_entity_manager:
                        parent = self.parent_entity_manager.get_entity(int(parent_id_str))
                    entity = self._entity_class.from_dict(int(entity_id_str), parent, data)
                    self._add_existing_entity(entity)

    def _add_existing_entity(self, entity):
        assert entity.entity_id is not None, "Entity id should not be None"
        self._entity_map[entity.entity_id] = entity

    def add_new_entity(self, parent_id: Optional[int], data: Dict[str, str]) -> Entity:
        entity_id = self._generate_entity_id()
        parent = None
        if self.parent_entity_manager:
            parent = self.parent_entity_manager.get_entity(parent_id)
        entity = self._entity_class.from_dict(entity_id, parent, data)
        self._entity_map[entity_id] = entity
        self._write_entities_to_file()
        return entity

    def modify_entity(self, entity_id: int, values: Dict[str, str]):
        entity = self.get_entity(entity_id)
        entity.modify(values)
        self._write_entities_to_file()

    def delete_entity(self, entity_id: int):
        entity = self.get_entity(entity_id)
        if self.children_entity_manager:
            entity_children = []
            for child in entity.children:
                entity_children.append(child)
            for child in entity_children:
                self.children_entity_manager.delete_entity(child.entity_id)
        if entity.parent:
            entity.parent.remove_child(entity)
        del self._entity_map[entity_id]
        self._write_entities_to_file()

    def _write_entities_to_file(self):
        sorted_entities = sorted(self._entity_map.values(), key=lambda cur_entity: cur_entity.entity_id)
        entity_dicts = []
        for entity in sorted_entities:
            entity_dicts.append(entity.to_dict())
        file_headers = self.entity_class.file_headers()
        with atomic_write(self.get_entities_file(), keep=False, owner=7, group=7, perms=7) as f:
            writer = csv.writer(f, dialect=csv.excel)
            writer.writerow(file_headers)
            for cur_dict in entity_dicts:
                row = []
                for header in file_headers:
                    row.append(cur_dict[header])
                writer.writerow(row)

    def _generate_entity_id(self):
        i = 1
        while i in self._entity_map:
            i += 1
        return i

    def get_entities(self):
        return sorted(self._entity_map.values(), key=lambda entity: entity.entity_id)

    def get_entity(self, entity_id: int):
        return self._entity_map[entity_id]
