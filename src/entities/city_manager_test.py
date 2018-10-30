import unittest
from .recipe import Recipe
from src.testing import test_utils


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_get_sorted_cookbooks(self):
        self.cookbook_manager.delete_entity(70)
        self.cookbook_manager.delete_entity(60)
        cookbook_1 = self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides(
            {"name": "Smitten kitchen"}))
        cookbook_2 = self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides(
            {"name": "Vietnamese Kitchen"}))
        cookbook_3 = self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides(
            {"name": "Food 52"}))
        self.assertEqual(self.cookbook_manager.get_sorted_cookbooks(), [cookbook_3, cookbook_1, cookbook_2])


if __name__ == '__main__':
    unittest.main()
