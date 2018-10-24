import unittest
from entities.entry import Entry


class TestEntry(unittest.TestCase):

    def test_setters(self):
        entry = Entry(0, 0, "default", 0, 0, "default", "default")
        entry.date = "2018-01-02"
        entry.id = 2
        entry.recipe_id = 7
        entry.miriam_rating = 9.5
        entry.james_rating = 9.1
        entry.miriam_comments = "Good"
        entry.james_comments = "Delicious"
        self.assertEqual(entry.id, 2)
        self.assertEqual(entry.recipe_id, 7)
        self.assertEqual(entry.date, "2018-01-02")
        self.assertAlmostEqual(entry.miriam_rating, 9.5)
        self.assertAlmostEqual(entry.james_rating, 9.1)
        self.assertEqual(entry.miriam_comments, "Good")
        self.assertEqual(entry.james_comments, "Delicious")

    def test_from_values(self):
        values = ["123", "234", "2018-01-02", "9.5", "9.1", "Good", "Delicious"]
        entry = Entry.from_values(values)
        self.assertEqual(entry.id, 123)
        self.assertEqual(entry.recipe_id, 234)
        self.assertEqual(entry.date, "2018-01-02")
        self.assertAlmostEqual(entry.miriam_rating, 9.5)
        self.assertAlmostEqual(entry.james_rating, 9.1)
        self.assertEqual(entry.miriam_comments, "Good")
        self.assertEqual(entry.james_comments, "Delicious")

    def test_to_line(self):
        entry = Entry(123, 234, "2018-01-02", 9.5, 9.1, "Good", "Delicious")
        self.assertEqual(entry.to_line(), "123,234,2018-01-02,9.5,9.1,Good,Delicious\n")

    def test_get_overall_rating_no_ratings_set(self):
        entry = Entry(0, 0, "default", 0, 0, "default", "default")
        self.assertAlmostEqual(entry.get_overall_rating(), 0)

    def test_get_overall_rating_miriam_rating_not_set(self):
        entry = Entry(0, 0, "default", 0, 5.6, "default", "default")
        self.assertAlmostEqual(entry.get_overall_rating(), 5.6)

    def test_get_overall_rating_james_rating_not_set(self):
        entry = Entry(0, 0, "default", 5.6, 0, "default", "default")
        self.assertAlmostEqual(entry.get_overall_rating(), 5.6)

    def test_get_overall_rating_both_ratings_set(self):
        entry = Entry(0, 0, "default", 5.6, 7.8, "default", "default")
        self.assertAlmostEqual(entry.get_overall_rating(), 6.7)


if __name__ == '__main__':
    unittest.main()
