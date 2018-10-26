import unittest
from .recipe import Recipe
from src.testing import test_utils


class TestRecipeManager(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_create_and_initialize_recipe_manager(self):
        recipes = self.recipe_manager.get_recipes()
        self.assertEqual(len(recipes), 2)
        self.assertEqual(recipes[0], Recipe(9, 7, "Chicken pot pie", 3, True, "Dinner", "Okay"))
        self.assertEqual(recipes[1], Recipe(8, 6, "Sashimi", 1, True, "Lunch", "Great"))
        self.assertEqual(self.cookbook_manager.get_cookbook(recipes[0].cookbook_id).recipes, [recipes[0]])
        self.assertEqual(self.cookbook_manager.get_cookbook(recipes[1].cookbook_id).recipes, [recipes[1]])

    def test_add_recipe(self):
        self.recipe_manager.add_new_recipe(
            self.cookbook_manager, "6", "Beef stew", "2", "Lunch", "Needs salt")
        self.recipe_manager.add_new_recipe(
            self.cookbook_manager, "6", "Steak", "0", "Dinner", "Not like a steakhouse")
        self.recipe_manager.add_new_recipe(
            self.cookbook_manager, "7", "Mushroom soup", "3", "Soup", "Too much garlic")
        recipes = self.recipe_manager.get_recipes()

        self.assertEqual(len(recipes), 5)
        self.assertEqual(recipes[0], Recipe(1, 6, "Beef stew", 2, False, "Lunch", "Needs salt"))
        self.assertEqual(recipes[1], Recipe(9, 7, "Chicken pot pie", 3, True, "Dinner", "Okay"))
        self.assertEqual(recipes[2], Recipe(3, 7, "Mushroom soup", 3, False, "Soup", "Too much garlic"))
        self.assertEqual(recipes[3], Recipe(8, 6, "Sashimi", 1, True, "Lunch", "Great"))
        self.assertEqual(recipes[4], Recipe(2, 6, "Steak", 0, False, "Dinner", "Not like a steakhouse"))
        self.assertEqual(sorted(self.cookbook_manager.get_cookbook(recipes[0].cookbook_id).recipes, \
                                key=lambda recipe: recipe.id), \
                         sorted([recipes[0], recipes[3], recipes[4]], key=lambda recipe: recipe.id))
        self.assertEqual(sorted(self.cookbook_manager.get_cookbook(recipes[1].cookbook_id).recipes, \
                                key=lambda recipe: recipe.id), \
                         sorted([recipes[1], recipes[2]], key=lambda recipe: recipe.id))


if __name__ == '__main__':
    unittest.main()
