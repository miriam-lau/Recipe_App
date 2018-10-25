import unittest
from .recipe_manager import RecipeManager
from .recipe import Recipe
from .cookbook_manager import CookbookManager


class TestRecipeManager(unittest.TestCase):

    def test_create_and_initialize_recipe_manager(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("src/testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "src/testing/recipes.txt")
        recipes = recipe_manager.get_recipes()
        self.assertEqual(len(recipes), 2)
        self.assertEqual(recipes[0], Recipe(9, 7, "Chicken pot pie", 3, True, "Dinner", "Okay"))
        self.assertEqual(recipes[1], Recipe(8, 6, "Sashimi", 1, True, "Lunch", "Great"))
        self.assertEqual(cookbook_manager.get_cookbook(recipes[0].cookbook_id).recipes, [recipes[0]])
        self.assertEqual(cookbook_manager.get_cookbook(recipes[1].cookbook_id).recipes, [recipes[1]])

    def test_add_recipe(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("src/testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "src/testing/recipes.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Beef stew", 2, True, "Lunch", "Needs salt"),
                                      "src/testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 6, "Steak", 0, False, "Dinner", \
                                                               "Not like a steakhouse"), "src/testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(cookbook_manager, Recipe(None, 7, "Mushroom soup", 3, False, "Soup", \
                                                               "Too much garlic"), "src/testing/test_add_recipe.txt")
        recipes = recipe_manager.get_recipes()

        self.assertEqual(len(recipes), 5)
        self.assertEqual(recipes[0], Recipe(1, 6, "Beef stew", 2, True, "Lunch", "Needs salt"))
        self.assertEqual(recipes[1], Recipe(9, 7, "Chicken pot pie", 3, True, "Dinner", "Okay"))
        self.assertEqual(recipes[2], Recipe(3, 7, "Mushroom soup", 3, False, "Soup", "Too much garlic"))
        self.assertEqual(recipes[3], Recipe(8, 6, "Sashimi", 1, True, "Lunch", "Great"))
        self.assertEqual(recipes[4], Recipe(2, 6, "Steak", 0, False, "Dinner", "Not like a steakhouse"))
        self.assertEqual(sorted(cookbook_manager.get_cookbook(recipes[0].cookbook_id).recipes, \
                                key=lambda recipe: recipe.id), \
                         sorted([recipes[0], recipes[3], recipes[4]], key=lambda recipe: recipe.id))
        self.assertEqual(sorted(cookbook_manager.get_cookbook(recipes[1].cookbook_id).recipes, \
                                key=lambda recipe: recipe.id), \
                         sorted([recipes[1], recipes[2]], key=lambda recipe: recipe.id))


if __name__ == '__main__':
    unittest.main()
