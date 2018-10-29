import unittest
from .recipe import Recipe
from src.testing import test_utils


class TestRecipeManager(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_get_image_filename(self):
        self.recipe_manager.add_new_entity(70,
                                           {"name": "Apple pie", "priority": "2", "has image": "True",
                                            "category": "Dessert", "notes": "Delicious"})
        self.assertEqual(self.recipe_manager.get_image_filename(1), "src/test_files/output/RecipeImages/1.jpg")


if __name__ == '__main__':
    unittest.main()
