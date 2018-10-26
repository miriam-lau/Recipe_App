import unittest
from .entry import Entry
import datetime
from src.testing import test_utils


class TestEntryManager(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_create_and_initialize_entry_manager(self):
        entries = self.entry_manager.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], Entry(10, 8, datetime.datetime(2018, 10, 22), 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[1], Entry(11, 9, datetime.datetime(2018, 1, 2), 4, 2, "Terrible", "Disgusting"))
        self.assertEqual(self.recipe_manager.get_recipe(entries[0].recipe_id).entries, [entries[0]])
        self.assertEqual(self.recipe_manager.get_recipe(entries[1].recipe_id).entries, [entries[1]])

    def test_add_entry(self):
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2017-05-24", "7", "6", "Okay", "Meh")
        self.entry_manager.add_new_entry(self.recipe_manager, "8", "2018-04-05", "2", "1", "Bland", "Gross")
        self.entry_manager.add_new_entry(self.recipe_manager, "9", "2018-07-19", "9", "8", "Excellent", "Good")
        entries = self.entry_manager.get_entries()

        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0], Entry(1, 8, datetime.datetime(2017, 5, 24), 7, 6, "Okay", "Meh"))
        self.assertEqual(entries[1], Entry(2, 8, datetime.datetime(2018, 4, 5), 2, 1, "Bland", "Gross"))
        self.assertEqual(entries[2], Entry(3, 9, datetime.datetime(2018, 7, 19), 9, 8, "Excellent", "Good"))
        self.assertEqual(entries[3], Entry(10, 8, datetime.datetime(2018, 10, 22), 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[4], Entry(11, 9, datetime.datetime(2018, 1, 2), 4, 2, "Terrible", "Disgusting"))
        self.assertEqual(sorted(
            self.recipe_manager.get_recipe(entries[0].recipe_id).entries, key=lambda entry: entry.id), \
                         sorted([entries[1], entries[3], entries[0]], key=lambda entry: entry.id))
        self.assertEqual(sorted(
            self.recipe_manager.get_recipe(entries[2].recipe_id).entries, key=lambda entry: entry.id), \
                         sorted([entries[4], entries[2]], key=lambda entry: entry.id))


if __name__ == '__main__':
    unittest.main()
