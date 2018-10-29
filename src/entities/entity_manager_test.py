import unittest
from src.testing.test_entity import TestEntity
from .entity_manager import EntityManager
from src.settings.settings import Settings
from src.testing import test_utils


class TestEntityManager(unittest.TestCase):

    def setUp(self):
        settings = Settings()
        settings.recipe_app_directory = "src/test_files/input/"
        self.parent_manager = EntityManager(TestEntity, settings, "empty entities.csv", "debug_entities.csv")
        self.child_manager = EntityManager(TestEntity, settings, "empty entities.csv", "debug_entities.csv")
        self.parent_manager.children_entity_manager = self.child_manager
        self.child_manager.parent_entity_manager = self.parent_manager
        self.parent_manager.initialize()
        self.child_manager.initialize()
        settings.recipe_app_directory = "src/test_files/output/"

    def test_initialize(self):
        settings = Settings()
        settings.recipe_app_directory = "src/test_files/input/"
        self.parent_manager = EntityManager(TestEntity, settings, "parent entities.csv", "debug_entities.csv")
        self.child_manager = EntityManager(TestEntity, settings, "child entities.csv", "debug_entities.csv")
        self.parent_manager.children_entity_manager = self.child_manager
        self.child_manager.parent_entity_manager = self.parent_manager
        self.parent_manager.initialize()
        self.child_manager.initialize()
        settings.recipe_app_directory = "src/test_files/output/"
        self.assertEqual(len(self.parent_manager.get_entities()), 2)
        self.assertEqual(len(self.child_manager.get_entities()), 2)
        self.assertEqual(
            self.parent_manager.get_entities()[0], TestEntity(60, None, {"name": "Parent 1", "notes": "P1 Notes"}))
        self.assertEqual(
            self.parent_manager.get_entities()[1], TestEntity(70, None, {"name": "Parent 2", "notes": "P2 Notes"}))
        self.assertEqual(
            self.child_manager.get_entities()[0], TestEntity(80, self.parent_manager.get_entities()[0],
                                                             {"name": "Child 1.1", "notes": "C1 Notes"}))
        self.assertEqual(
            self.child_manager.get_entities()[1], TestEntity(90, self.parent_manager.get_entities()[1],
                                                             {"name": "Child 2.1", "notes": "C2 Notes"}))

    def test_add_new_entity(self):
        self.parent_manager.add_new_entity(None, {"name": "Joy of Cooking", "notes": "Amazing"})
        self.child_manager.add_new_entity(1, {"name": "Chicken pot pie", "notes": "Delicious"})
        self.assertEqual(len(self.parent_manager.get_entities()), 1)
        self.assertEqual(len(self.child_manager.get_entities()), 1)
        self.assertEqual(
            self.parent_manager.get_entities()[0], TestEntity(1, None, {"name": "Joy of Cooking", "notes": "Amazing"}))
        self.assertEqual(
            self.child_manager.get_entities()[0], TestEntity(1, self.parent_manager.get_entities()[0],
                                                             {"name": "Chicken pot pie", "notes": "Delicious"}))

    def test_modify_entity(self):
        self.parent_manager.add_new_entity(None, {"name": "Joy of Cooking", "notes": "Amazing"})
        self.parent_manager.modify_entity(1, {"name": "Good Eats", "notes": "Terrible"})
        self.assertEqual(len(self.parent_manager.get_entities()), 1)
        self.assertEqual(
            self.parent_manager.get_entities()[0], TestEntity(1, None, {"name": "Good Eats", "notes": "Terrible"}))

    def test_delete_entity(self):
        self.parent_manager.add_new_entity(None, {"name": "Joy of Cooking", "notes": "Amazing"})
        self.parent_manager.delete_entity(1)
        self.assertEqual(len(self.parent_manager.get_entities()), 0)

    def test_get_entities(self):
        self.parent_manager.add_new_entity(None, {"name": "Joy of Cooking", "notes": "Amazing"})
        self.parent_manager.add_new_entity(None, {"name": "Good Eats", "notes": "Terrible"})
        self.assertEqual(len(self.parent_manager.get_entities()), 2)
        self.assertEqual(
            self.parent_manager.get_entities()[0], TestEntity(1, None, {"name": "Joy of Cooking", "notes": "Amazing"}))
        self.assertEqual(
            self.parent_manager.get_entities()[1], TestEntity(2, None, {"name": "Good Eats", "notes": "Terrible"}))

    def test_get_entity(self):
        self.parent_manager.add_new_entity(None, {"name": "Joy of Cooking", "notes": "Amazing"})
        self.parent_manager.add_new_entity(None, {"name": "Good Eats", "notes": "Terrible"})
        self.assertEqual(
            self.parent_manager.get_entity(2), TestEntity(2, None, {"name": "Good Eats", "notes": "Terrible"}))


if __name__ == '__main__':
    unittest.main()
