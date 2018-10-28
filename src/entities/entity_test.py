import unittest
from .entity import Entity


class TestEntity(unittest.TestCase):

    def test_add_child(self):
        parent_entity = Entity(1, 2)
        child_entity = Entity(1, 3)
        parent_entity.add_child(child_entity)
        self.assertEqual(len(parent_entity.children), 1)
        self.assertEqual(parent_entity.children[0], child_entity)

    def test_remove_child(self):
        parent_entity = Entity(1, 2)
        child_entity_1 = Entity(1, 3)
        child_entity_2 = Entity(1, 4)
        parent_entity.add_child(child_entity_1)
        parent_entity.add_child(child_entity_2)
        parent_entity.remove_child(child_entity_1)
        self.assertEqual(len(parent_entity.children), 1)
        self.assertEqual(parent_entity.children[0], child_entity_2)


if __name__ == '__main__':
    unittest.main()
