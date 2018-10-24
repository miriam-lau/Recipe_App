import unittest
from entities.entry_manager import EntryManager
from entities.entry import Entry
from entities.recipe_manager import RecipeManager
from entities.cookbook_manager import CookbookManager
import datetime


class TestEntryManager(unittest.TestCase):

    def test_create_and_initialize_entry_manager(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        entries = entry_manager.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], Entry(10, 8, datetime.datetime(2018, 10, 22), 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[1], Entry(11, 9, datetime.datetime(2018, 1, 2), 4, 2, "Terrible", "Disgusting"))
        self.assertEqual(recipe_manager.get_recipe(entries[0].recipe_id).entries, [entries[0]])
        self.assertEqual(recipe_manager.get_recipe(entries[1].recipe_id).entries, [entries[1]])

    def test_add_entry(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        recipe_manager = RecipeManager.create_and_initialize_recipe_manager(cookbook_manager, "testing/recipes.txt")
        entry_manager = EntryManager.create_and_initialize_entry_manager(recipe_manager, "testing/entries.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"), \
            "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 8, datetime.datetime(2018, 4, 5), 2, 1, "Bland", "Gross"), \
            "testing/test_add_entry.txt")
        entry_manager.add_new_entry(
            recipe_manager, Entry(None, 9, datetime.datetime(2018, 7, 19), 9, 8, "Excellent", "Good"), \
            "testing/test_add_entry.txt")
        entries = entry_manager.get_entries()

        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0], Entry(1, 8, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"))
        self.assertEqual(entries[1], Entry(2, 8, datetime.datetime(2018, 4, 5), 2, 1, "Bland", "Gross"))
        self.assertEqual(entries[2], Entry(3, 9, datetime.datetime(2018, 7, 19), 9, 8, "Excellent", "Good"))
        self.assertEqual(entries[3], Entry(10, 8, datetime.datetime(2018, 10, 22), 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[4], Entry(11, 9, datetime.datetime(2018, 1, 2), 4, 2, "Terrible", "Disgusting"))
        self.assertEqual(sorted(recipe_manager.get_recipe(entries[0].recipe_id).entries, key=lambda entry: entry.id), \
                         sorted([entries[1], entries[3], entries[0]], key=lambda entry: entry.id))
        self.assertEqual(sorted(recipe_manager.get_recipe(entries[2].recipe_id).entries, key=lambda entry: entry.id), \
                         sorted([entries[4], entries[2]], key=lambda entry: entry.id))


if __name__ == '__main__':
    unittest.main()
