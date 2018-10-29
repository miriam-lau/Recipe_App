import unittest
from .recipe import Recipe
from src.testing import test_utils


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_from_dict(self):
        recipe = Recipe.from_dict(1, self.cookbook_manager.get_entity(70),
                                  {"name": "Apple pie", "priority": "2", "has image": "True",
                                   "category": "Dessert", "notes": "Delicious"})
        self.assertEqual(recipe.entity_id, 1)
        self.assertEqual(recipe.parent_id, 70)
        self.assertEqual(recipe.name, "Apple pie")
        self.assertEqual(recipe.priority, 2)
        self.assertEqual(recipe.has_image, True)
        self.assertEqual(recipe.category, "Dessert")
        self.assertEqual(recipe.notes, "Delicious")

    def test_to_dict(self):
        recipe = Recipe(1, self.cookbook_manager.get_entity(70),
                        {"name": "Apple pie", "priority": "2", "has image": "True",
                         "category": "Dessert", "notes": "Delicious"})
        self.assertEqual(recipe.to_dict(), {
            "entity id": "1", "parent id": "70", "name": "Apple pie", "priority": "2", "has image": "True",
                         "category": "Dessert", "notes": "Delicious"})

    def test_modify(self):
        recipe = Recipe(1, self.cookbook_manager.get_entity(70),
                        {"name": "Apple pie", "priority": "2", "has image": "True",
                         "category": "Dessert", "notes": "Delicious"})
        update_dict = {
            Recipe.NAME_HEADER: "Ice cream",
            Recipe.PRIORITY_HEADER: "3",
            Recipe.HAS_IMAGE_HEADER: "False",
            Recipe.CATEGORY_HEADER: "Dairy",
            Recipe.NOTES_HEADER: "Good",
        }
        recipe.modify(update_dict)
        self.assertEqual(recipe.entity_id, 1)
        self.assertEqual(recipe.parent_id, 70)
        self.assertEqual(recipe.name, "Ice cream")
        self.assertEqual(recipe.priority, 3)
        self.assertEqual(recipe.has_image, False)
        self.assertEqual(recipe.category, "Dairy")
        self.assertEqual(recipe.notes, "Good")

    def test_file_headers(self):
        self.assertEqual(Recipe.file_headers(), ["entity id", "parent id", "name", "priority", "has image",
                                                 "category", "notes"])

    def test_get_num_times_made(self):
        self.recipe_manager.add_new_entity(70, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        recipe = self.recipe_manager.get_entity(1)
        self.assertEqual(recipe.get_num_times_made(), 3)

    def test_get_best_rating(self):
        self.recipe_manager.add_new_entity(70, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "9.5", "james rating": "9.1"}))
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        recipe = self.recipe_manager.get_entity(1)
        self.assertAlmostEqual(recipe.get_best_rating(), 9.3)

    def test_get_latest_rating(self):
        self.recipe_manager.add_new_entity(70, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-05", "miriam rating": "9.5", "james rating": "9.1"}))
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-08", "miriam rating": "5.5", "james rating": "5.1"}))
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-02", "miriam rating": "7.5", "james rating": "7.1"}))
        recipe = self.recipe_manager.get_entity(1)
        self.assertAlmostEqual(recipe.get_latest_rating(), 5.3)

    def test_entries_by_date_descending(self):
        self.recipe_manager.add_new_entity(70, test_utils.default_recipe_dict_with_overrides())
        entry_1 = self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-05", "miriam rating": "9.5", "james rating": "9.1"}))
        entry_2 = self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-08", "miriam rating": "5.5", "james rating": "5.1"}))
        entry_3 = self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"date": "2018-10-02", "miriam rating": "7.5", "james rating": "7.1"}))
        recipe = self.recipe_manager.get_entity(1)
        self.assertEqual(recipe.entries_by_date_descending(), [entry_2, entry_1, entry_3])


if __name__ == '__main__':
    unittest.main()
