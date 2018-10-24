import unittest
from .cookbook import Cookbook
from .entry_manager import EntryManager
from .recipe_manager import RecipeManager
from .recipe import Recipe
from .entry import Entry
from .cookbook_manager import CookbookManager
import datetime


class TestCookbook(unittest.TestCase):

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
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Beef stew", 2, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Test", 2, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 1, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"), \
            "testing/test_add_entry.txt")
        cookbook = cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.num_recipes_made(), 2)

    def test_num_recipes_want_to_make(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Beef stew", 2, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Test", 0, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 1, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"), \
            "testing/test_add_entry.txt")
        cookbook = cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.num_recipes_want_to_make(), 2)

    def test_success_percentage(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Beef stew", 2, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Test", 0, True, "Lunch", "Needs salt"),
                                      "testing/test_add_recipe.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 1, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"), \
            "testing/test_add_entry.txt")
        cookbook = cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook.success_percentage(), 50)


if __name__ == '__main__':
    unittest.main()
