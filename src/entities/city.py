from __future__ import annotations
from typing import Dict, List
from .entity import Entity
from .restaurant import Restaurant


class City(Entity):

    NAME_HEADER = "name"
    STATE_HEADER = "state"
    COUNTRY_HEADER = "country"
    NOTES_HEADER = "notes"

    def __init__(self, entity_id, data: Dict[str, str]):
        Entity.__init__(self, entity_id, None)
        self.name: str = None
        self.state: str = None
        self.country: str = None
        self.notes: str = None
        self.modify(data)

    @staticmethod
    def from_dict(entity_id, parent_unused, data) -> City:
        return City(entity_id, data)

    def to_dict(self):
        return {
            Entity.ENTITY_ID_HEADER: str(self.entity_id),
            Entity.PARENT_ID_HEADER: "0",
            City.NAME_HEADER: self.name,
            City.STATE_HEADER: self.state,
            City.COUNTRY_HEADER: self.country,
            City.NOTES_HEADER: self.notes
        }

    def modify(self, data):
        if City.NAME_HEADER in data:
            self.name = data[City.NAME_HEADER]
        if City.STATE_HEADER in data:
            self.state = data[City.STATE_HEADER]
        if City.COUNTRY_HEADER in data:
            self.country = data[City.COUNTRY_HEADER]
        if City.NOTES_HEADER in data:
            self.notes = data[City.NOTES_HEADER]

    @staticmethod
    def file_headers():
        return [Entity.ENTITY_ID_HEADER, Entity.PARENT_ID_HEADER, City.NAME_HEADER, City.STATE_HEADER,
                City.COUNTRY_HEADER, City.NOTES_HEADER]

    @property
    def restaurants(self):
        return self._children

    def restaurants_by_best_rating_descending(self) -> List[Restaurant]:
        return sorted(self.restaurants, key=lambda restaurant: restaurant.get_best_rating(), reverse=True)

    def __str__(self):
        return "entity id: %s, name: %s, state %s, country %s, notes: %s" % (
            self.entity_id, self.name, self.state, self.country, self.notes)

    # For unit testing.
    def __eq__(self, other):
        return self.entity_id == other.entity_id and self.name == other.name and \
               self.state == other.state and self.country == other.country and self.notes == other.notes
