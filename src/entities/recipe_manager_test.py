import unittest
from entities.recipe_manager import RecipeManager
from entities.recipe import Recipe



class TestRecipeManager(unittest.TestCase):

    def test_create_and_initialize_recipe_manager(self):
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager("testing/recipes.txt")
        recipes = recipe_manager.get_recipes()
        self.assertEqual(len(recipes), 2)
        self.assertEqual(recipes[0], Recipe(4, 7, "Chicken pot pie", 3, "chicken.jpg", "Dinner"))
        self.assertEqual(recipes[1], Recipe(2, 6, "Sashimi", 1, "sashimi.jpg", "Lunch"))

    def test_add_recipe(self):
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager("testing/recipes.txt")
        recipe_manager.add_new_recipe(Recipe(None, 5, "Beef stew", 2, "beef.jpg","Lunch"),
                                      "testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(Recipe(None, 5, "Steak", 0, "steak.jpg", "Dinner"), "testing/test_add_recipe.txt")
        recipe_manager.add_new_recipe(Recipe(None, 7, "Mushroom soup", 3, "mushroomsoup.jpg", "Soup"),
                                      "testing/test_add_recipe.txt")
        recipes = recipe_manager.get_recipes()

        self.assertEqual(len(recipes), 5)
        self.assertEqual(recipes[0], Recipe(1, 5, "Beef stew", 2, "beef.jpg", "Lunch"))
        self.assertEqual(recipes[1], Recipe(4, 7, "Chicken pot pie", 3, "chicken.jpg", "Dinner"))
        self.assertEqual(recipes[2], Recipe(5, 7, "Mushroom soup", 3, "mushroomsoup.jpg", "Soup"))
        self.assertEqual(recipes[3], Recipe(2, 6, "Sashimi", 1, "sashimi.jpg", "Lunch"))
        self.assertEqual(recipes[4], Recipe(3, 5, "Steak", 0, "steak.jpg", "Dinner"))

    def test_get_recipes_for_cookbook(self):
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager("testing/recipes.txt")
        recipes = recipe_manager.get_recipes_for_cookbook(7)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0], Recipe(4, 7, "Chicken pot pie", 3, "chicken.jpg", "Dinner"))


if __name__ == '__main__':
    unittest.main()
