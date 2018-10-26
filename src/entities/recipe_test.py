import unittest
from .entry_manager import EntryManager
from .recipe_manager import RecipeManager
from .recipe import Recipe
from .entry import Entry
from .cookbook_manager import CookbookManager
import datetime
from src.testing import test_utils


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_from_values(self):
        values = ["123", "234", "Chicken pot pie", "3", "True", "Lunch", "Okay"]
        recipe = Recipe.from_values(values)
        self.assertEqual(recipe.id, 123)
        self.assertEqual(recipe.cookbook_id, 234)
        self.assertEqual(recipe.name, "Chicken pot pie")
        self.assertEqual(recipe.priority, 3)
        self.assertEqual(recipe.has_image, True)
        self.assertEqual(recipe.category, "Lunch")
        self.assertEqual(recipe.notes, "Okay")

    def test_to_tuple(self):
        recipe = Recipe(123, 234, "Chicken pot pie", 3, True, "Lunch", "Okay")
        self.assertEqual(recipe.to_tuple(), (123, 234, "Chicken pot pie", 3, True, "Lunch", "Okay"))

    def test_get_num_times_made(self):
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        recipe = self.recipe_manager.get_recipe(8)
        self.assertEqual(recipe.get_num_times_made(), 4)

    def test_get_best_rating(self):
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        recipe = self.recipe_manager.get_recipe(8)
        self.assertAlmostEqual(recipe.get_best_rating(), 9.3)

    def test_get_latest_rating(self):
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2018-10-23", "3", "4", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        recipe = self.recipe_manager.get_recipe(8)
        self.assertAlmostEqual(recipe.get_latest_rating(), 3.5)


if __name__ == '__main__':
    unittest.main()
