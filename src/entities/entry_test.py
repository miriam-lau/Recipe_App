import unittest
from .entry import Entry
import datetime
from src.testing import test_utils


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.cookbook_manager, self.recipe_manager, self.entry_manager, self.settings = \
            test_utils.initialize_test_environment()

    def test_from_dict(self):
        entry = Entry.from_dict(1, self.recipe_manager.get_entity(90),
                                {"date": "2018-01-02", "miriam rating": "9.5", "james rating": "9.1",
                                 "miriam comments": "Good", "james comments": "Delicious"})
        self.assertEqual(entry.entity_id, 1)
        self.assertEqual(entry.parent_id, 90)
        self.assertEqual(entry.date, datetime.datetime(2018, 1, 2))
        self.assertAlmostEqual(entry.miriam_rating, 9.5)
        self.assertAlmostEqual(entry.james_rating, 9.1)
        self.assertEqual(entry.miriam_comments, "Good")
        self.assertEqual(entry.james_comments, "Delicious")

    def test_to_dict(self):
        entry = Entry(1, self.recipe_manager.get_entity(90),
                      {"date": "2018-01-02", "miriam rating": "9.5", "james rating": "9.1",
                       "miriam comments": "Good", "james comments": "Delicious"})
        self.assertEqual(entry.to_dict(), {
            "entity id": "1", "parent id": "90", "date": "2018-01-02", "miriam rating": "9.5",
            "james rating": "9.1", "miriam comments": "Good", "james comments": "Delicious"})

    def test_modify(self):
        entry = Entry(1, self.recipe_manager.get_entity(90),
                      {"date": "2018-01-02", "miriam rating": "9.5", "james rating": "9.1",
                       "miriam comments": "Good", "james comments": "Delicious"})
        update_dict = {
            Entry.DATE_HEADER: "2018-02-03",
            Entry.MIRIAM_RATING_HEADER: "8.5",
            Entry.JAMES_RATING_HEADER: "8.1",
            Entry.MIRIAM_COMMENTS_HEADER: "Worse",
            Entry.JAMES_COMMENTS_HEADER: "Bad",
        }
        entry.modify(update_dict)
        self.assertEqual(entry.entity_id, 1)
        self.assertEqual(entry.parent_id, 90)
        self.assertEqual(entry.date, datetime.datetime(2018, 2, 3))
        self.assertAlmostEqual(entry.miriam_rating, 8.5)
        self.assertAlmostEqual(entry.james_rating, 8.1)
        self.assertEqual(entry.miriam_comments, "Worse")
        self.assertEqual(entry.james_comments, "Bad")

    def test_file_headers(self):
        self.assertEqual(Entry.file_headers(), ["entity id", "parent id", "date", "miriam rating",
                                                "james rating", "miriam comments", "james comments"])

    def test_get_overall_rating_no_ratings_set(self):
        entry = self.entry_manager.add_new_entity(90, test_utils.default_entry_dict_with_overrides({
            "james rating": "0",
            "miriam rating": "0",
        }))
        self.assertAlmostEqual(entry.get_overall_rating(), 0)

    def test_get_overall_rating_miriam_rating_not_set(self):
        entry = self.entry_manager.add_new_entity(90, test_utils.default_entry_dict_with_overrides({
            "james rating": "5.6",
            "miriam rating": "0",
        }))
        self.assertAlmostEqual(entry.get_overall_rating(), 5.6)

    def test_get_overall_rating_james_rating_not_set(self):
        entry = self.entry_manager.add_new_entity(90, test_utils.default_entry_dict_with_overrides({
            "james rating": "0",
            "miriam rating": "5.6",
        }))
        self.assertAlmostEqual(entry.get_overall_rating(), 5.6)

    def test_get_overall_rating_both_ratings_set(self):
        entry = self.entry_manager.add_new_entity(90, test_utils.default_entry_dict_with_overrides({
            "james rating": "7.8",
            "miriam rating": "5.6",
        }))
        self.assertAlmostEqual(entry.get_overall_rating(), 6.7)


if __name__ == '__main__':
    unittest.main()
