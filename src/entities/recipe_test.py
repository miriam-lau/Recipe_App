import unittest
from entities.entry_manager import EntryManager
from entities.recipe_manager import RecipeManager
from entities.recipe import Recipe
from entities.entry import Entry
from entities.cookbook_manager import CookbookManager


class TestRecipe(unittest.TestCase):

    def test_setters(self):
        recipe = Recipe(0, 0, "default", 0, False, "default", "default")
        recipe.name = "changed_name"
        recipe.id = 2
        recipe.cookbook_id = 7
        recipe.priority = 3
        recipe.has_image = True
        recipe.category = "Breakfast"
        recipe.notes = "Okay"
        self.assertEqual(recipe.id, 2)
        self.assertEqual(recipe.cookbook_id, 7)
        self.assertEqual(recipe.name, "changed_name")
        self.assertEqual(recipe.category, "Breakfast")
        self.assertEqual(recipe.priority, 3)
        self.assertEqual(recipe.has_image, True)
        self.assertEqual(recipe.notes, "Okay")

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
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        recipe = recipe_manager.get_recipe(8)
        self.assertEqual(recipe.get_num_times_made(), 4)

    def test_get_best_rating(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        recipe = recipe_manager.get_recipe(8)
        self.assertAlmostEqual(recipe.get_best_rating(), 9.3)


if __name__ == '__main__':
    unittest.main()
