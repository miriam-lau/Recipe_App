import unittest
from entities.recipe import Recipe


class TestRecipe(unittest.TestCase):

    def test_setters(self):
        recipe = Recipe(0, 0, "default", 0, "default", "default")
        recipe.name = "changed_name"
        recipe.id = 2
        recipe.cookbook_id = 7
        recipe.priority = 3
        recipe.image = "image.jpg"
        recipe.category = "Breakfast"
        self.assertEqual(recipe.id, 2)
        self.assertEqual(recipe.cookbook_id, 7)
        self.assertEqual(recipe.name, "changed_name")
        self.assertEqual(recipe.category, "Breakfast")
        self.assertEqual(recipe.priority, 3)
        self.assertEqual(recipe.image, "image.jpg")

    def test_from_line(self):
        line = "123,234,Chicken pot pie,3,image.jpg,Lunch\n"
        recipe = Recipe.from_line(line)
        self.assertEqual(recipe.id, 123)
        self.assertEqual(recipe.cookbook_id, 234)
        self.assertEqual(recipe.name, "Chicken pot pie")
        self.assertEqual(recipe.priority, 3)
        self.assertEqual(recipe.image, "image.jpg")
        self.assertEqual(recipe.category, "Lunch")

    def test_to_line(self):
        recipe = Recipe(123, 234, "Chicken pot pie", 3, "image.jpg", "Lunch")
        self.assertEqual(recipe.to_line(), "123,234,Chicken pot pie,3,image.jpg,Lunch\n")


if __name__ == '__main__':
    unittest.main()
