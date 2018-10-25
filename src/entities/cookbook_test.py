import unittest
from .cookbook import Cookbook
from .entry_manager import EntryManager
from .recipe_manager import RecipeManager
from .recipe import Recipe
from .entry import Entry
from .cookbook_manager import CookbookManager
import datetime
from src.testing import test_utils


class TestCookbook(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_setters(self):
        cookbook = Cookbook(1, "default", "default")
        cookbook.name = "changed_name"
        cookbook.id = 2
        cookbook.notes = "Okay"
        self.assertEqual(cookbook.id, 2)
        self.assertEqual(cookbook.name, "changed_name")
        self.assertEqual(cookbook.notes, "Okay")

    def test_from_values(self):
        values = ["123", "Harry Potter Cookbook", "Magical"]
        cookbook = Cookbook.from_values(values)
        self.assertEqual(cookbook.id, 123)
        self.assertEqual(cookbook.name, "Harry Potter Cookbook")
        self.assertEqual(cookbook.notes, "Magical")

    def test_to_tuple(self):
        cookbook = Cookbook(123, "Harry Potter Cookbook", "Magical")
        self.assertEqual(cookbook.to_tuple(), (123, "Harry Potter Cookbook", "Magical"))

    def test_num_recipes_made(self):
        cookbook = Cookbook(1, "default", "default")
        cookbook.name = "changed_name"
        cookbook.id = 2
        cookbook.notes = "Okay"
        self.assertEqual(cookbook.id, 2)
        self.assertEqual(cookbook.name, "changed_name")
        self.assertEqual(cookbook.notes, "Okay")

    def test_num_recipes_made(self):
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Beef stew", "2", "Lunch", "Needs salt")
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Test", "2", "Lunch", "Needs salt")
        self.entry_manager.add_new_entry(self.recipe_manager, "1", "2017-05-24", "7", "6", "Okay", "Meh")
        cookbook = self.cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.num_recipes_made(), 2)

    def test_num_recipes_want_to_make(self):
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Beef stew", "2", "Lunch", "Needs salt")
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Test", "0", "Lunch", "Needs salt")
        self.entry_manager.add_new_entry(self.recipe_manager, "1", "2017-05-24", "7", "6", "Okay", "Meh")
        cookbook = self.cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.num_recipes_want_to_make(), 2)

    def test_success_percentage(self):
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Beef stew", "2", "Lunch", "Needs salt")
        self.recipe_manager.add_new_recipe(self.cookbook_manager, "6", "Test", "0", "Lunch", "Needs salt")
        self.entry_manager.add_new_entry(self.recipe_manager, "1", "2017-05-24", "7", "6", "Okay", "Meh")
        cookbook = self.cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.success_percentage(), 50)


if __name__ == '__main__':
    unittest.main()
