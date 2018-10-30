import unittest
from .cookbook import Cookbook
from src.testing import test_utils


class TestCookbook(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_from_dict(self):
        cookbook = Cookbook.from_dict(1, 0, {"name": "Harry Potter Cookbook", "notes": "Magical"})
        self.assertEqual(cookbook.entity_id, 1)
        self.assertEqual(cookbook.name, "Harry Potter Cookbook")
        self.assertEqual(cookbook.notes, "Magical")

    def test_to_dict(self):
        cookbook = Cookbook(1, {"name": "Harry Potter Cookbook", "notes": "Magical"})
        self.assertEqual(cookbook.to_dict(), {
            "entity id": "1", "parent id": "0", "name": "Harry Potter Cookbook", "notes": "Magical"})

    def test_modify(self):
        cookbook = Cookbook(1, test_utils.default_cookbook_dict_with_overrides())
        update_dict = {
            Cookbook.NAME_HEADER: "Joy of cooking",
            Cookbook.NOTES_HEADER: "Amazing"
        }
        cookbook.modify(update_dict)
        self.assertEqual(cookbook.name, "Joy of cooking")
        self.assertEqual(cookbook.notes, "Amazing")

    def test_file_headers(self):
        self.assertEqual(Cookbook.file_headers(), ["entity id", "parent id", "name", "notes"])


if __name__ == '__main__':
    unittest.main()
