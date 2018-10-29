import unittest
from .cookbook import Cookbook
from src.testing import test_utils


class TestCookbook(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_from_dict(self):
        cookbook = Cookbook.from_dict(1, 0, {"name": "Harry Potter Cookbook", "notes": "Magical"})
        self.assertEqual(cookbook.entity_id, 1)
        self.assertEqual(cookbook.name, "Harry Potter Cookbook")
        self.assertEqual(cookbook.notes, "Magical")

    def test_to_dict(self):
        cookbook = Cookbook(1, {"name": "Harry Potter Cookbook", "notes": "Magical"})
        self.assertEqual(cookbook.to_dict(), {
            "entity id": "1", "parent id": "0", "name": "Harry Potter Cookbook", "notes": "Magical"})

    def test_modify(self):
        cookbook = Cookbook(1, test_utils.default_cookbook_dict_with_overrides())
        update_dict = {
            Cookbook.NAME_HEADER: "Joy of cooking",
            Cookbook.NOTES_HEADER: "Amazing"
        }
        cookbook.modify(update_dict)
        self.assertEqual(cookbook.name, "Joy of cooking")
        self.assertEqual(cookbook.notes, "Amazing")

    def test_num_recipes_made(self):
        self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides())
        self.entry_manager.add_new_entity(3, test_utils.default_entry_dict_with_overrides())
        cookbook = self.cookbook_manager.get_entity(1)
        self.assertEqual(cookbook.num_recipes_made(), 2)

    def test_num_recipes_want_to_make(self):
        self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides({"priority": "4"}))
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides({"priority": "0"}))
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides({"priority": "1"}))
        cookbook = self.cookbook_manager.get_entity(1)
        self.assertEqual(cookbook.num_recipes_want_to_make(), 2)

    def test_success_percentage(self):
        self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "7.0", "james rating": "8.0"}))
        self.entry_manager.add_new_entity(2, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "2.0", "james rating": "3.0"}))
        self.entry_manager.add_new_entity(3, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "9.0", "james rating": "9.0"}))
        self.entry_manager.add_new_entity(4, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "3.0", "james rating": "6.0"}))
        cookbook = self.cookbook_manager.get_entity(1)
        self.assertEqual(cookbook.success_percentage(), 50)

    def test_recipes_by_best_rating_descending(self):
        self.cookbook_manager.add_new_entity(None, test_utils.default_cookbook_dict_with_overrides())
        recipe_1 = self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        recipe_2 = self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        recipe_3 = self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        recipe_4 = self.recipe_manager.add_new_entity(1, test_utils.default_recipe_dict_with_overrides())
        self.entry_manager.add_new_entity(1, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "5.0", "james rating": "5.0"}))
        self.entry_manager.add_new_entity(2, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "9.0", "james rating": "9.0"}))
        self.entry_manager.add_new_entity(3, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "2.0", "james rating": "2.0"}))
        self.entry_manager.add_new_entity(4, test_utils.default_entry_dict_with_overrides(
            {"miriam rating": "7.0", "james rating": "7.0"}))
        cookbook = self.cookbook_manager.get_entity(1)
        self.assertEqual(cookbook.recipes_by_best_rating_descending(), [recipe_2, recipe_4, recipe_1, recipe_3])
        self.assertEqual(cookbook.success_percentage(), 50)

    def test_file_headers(self):
        self.assertEqual(Cookbook.file_headers(), ["entity id", "parent id", "name", "notes"])


if __name__ == '__main__':
    unittest.main()
