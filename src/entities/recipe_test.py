import unittest
from entities.recipe import Recipe


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


if __name__ == '__main__':
    unittest.main()
