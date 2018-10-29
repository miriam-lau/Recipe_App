import unittest
from .entity import Entity


class TestEntity(unittest.TestCase):

    def test_add_child(self):
        parent_entity = Entity(1, None)
        child_entity = Entity(1, parent_entity)
        self.assertEqual(len(parent_entity.children), 1)
        self.assertEqual(parent_entity.children[0], child_entity)
        self.assertEqual(child_entity.parent, parent_entity)

    def test_remove_child(self):
        parent_entity = Entity(1, None)
        child_entity_1 = Entity(1, parent_entity)
        child_entity_2 = Entity(1, parent_entity)
        parent_entity.remove_child(child_entity_1)
        self.assertEqual(len(parent_entity.children), 1)
        self.assertEqual(parent_entity.children[0], child_entity_2)
        self.assertEqual(child_entity_1.parent, parent_entity)
        self.assertEqual(child_entity_2.parent, parent_entity)


if __name__ == '__main__':
    unittest.main()
