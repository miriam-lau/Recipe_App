import unittest
from entities.entry_manager import EntryManager
from entities.entry import Entry


class TestEntryManager(unittest.TestCase):

    def test_create_and_initialize_entry_manager(self):
        entry_manager = EntryManager.create_and_initialize_entry_manager("testing/entries.txt")
        entries = entry_manager.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], Entry(2, 6, "2018-10-22", 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[1], Entry(4, 7, "2018-01-02", 4, 2, "Terrible", "Disgusting"))

    def test_add_entry(self):
        entry_manager = EntryManager.create_and_initialize_entry_manager("testing/entries.txt")
        entry_manager.add_new_entry(Entry(None, 5, "2017-05-24", 7, 6, "Okay", "Meh"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(Entry(None, 5, "2018-04-05", 2, 1, "Bland", "Gross"), "testing/test_add_entry.txt")
        entry_manager.add_new_entry(Entry(None, 7, "2018-07-19", 9, 8, "Excellent", "Good"), \
                                    "testing/test_add_entry.txt")
        entries = entry_manager.get_entries()

        self.assertEqual(len(entries), 5)
        self.assertEqual(entries[0], Entry(1, 5, "2017-05-24", 7, 6, "Okay", "Meh"))
        self.assertEqual(entries[1], Entry(2, 6, "2018-10-22", 9.5, 9.1, "Good", "Delicious"))
        self.assertEqual(entries[2], Entry(3, 5, "2018-04-05", 2, 1, "Bland", "Gross"))
        self.assertEqual(entries[3], Entry(4, 7, "2018-01-02", 4, 2, "Terrible", "Disgusting"))
        self.assertEqual(entries[4], Entry(5, 7, "2018-07-19", 9, 8, "Excellent", "Good"))

    def test_get_entries_for_cookbook(self):
        entry_manager = EntryManager.create_and_initialize_entry_manager("testing/entries.txt")
        entries = entry_manager.get_entries_for_recipe(7)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], Entry(4, 7, "2018-01-02", 4, 2, "Terrible", "Disgusting"))


if __name__ == '__main__':
    unittest.main()
