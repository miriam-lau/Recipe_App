import unittest
from .cookbook_manager import CookbookManager
from .cookbook import Cookbook
from src.settings.settings import Settings
from src.testing import test_utils


class TestCookbookManager(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_create_and_initialize_cookbook_manager(self):
        cookbooks = self.cookbook_manager.get_cookbooks()
        self.assertEqual(len(cookbooks), 2)
        self.assertEqual(cookbooks[0], Cookbook(7, "Joy of Cooking", "Great"))
        self.assertEqual(cookbooks[1], Cookbook(6, "Momofuku", "Okay"))

    def test_add_cookbook(self):
        self.cookbook_manager.add_new_cookbook("Atelier Crenn", "Superb")
        self.cookbook_manager.add_new_cookbook("Smitten Kitchen", "Meh")
        self.cookbook_manager.add_new_cookbook("America's Test Kitchen", "Bad")
        cookbooks = self.cookbook_manager.get_cookbooks()

        self.assertEqual(len(cookbooks), 5)
        self.assertEqual(cookbooks[0], Cookbook(3, "America's Test Kitchen", "Bad"))
        self.assertEqual(cookbooks[1], Cookbook(1, "Atelier Crenn", "Superb"))
        self.assertEqual(cookbooks[2], Cookbook(7, "Joy of Cooking", "Great"))
        self.assertEqual(cookbooks[3], Cookbook(6, "Momofuku", "Okay"))
        self.assertEqual(cookbooks[4], Cookbook(2, "Smitten Kitchen", "Meh"))

    def test_get_cookbook(self):
        cookbook = self.cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook, Cookbook(6, "Momofuku", "Okay"))


if __name__ == '__main__':
    unittest.main()
