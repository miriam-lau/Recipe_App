import unittest
from entities.cookbook import Cookbook


class TestCookbook(unittest.TestCase):

    def test_setters(self):
        cookbook = Cookbook(1, "default", "default")
        cookbook.name = "changed_name"
        cookbook.id = 2
        cookbook.notes = "Okay"
        self.assertEqual(cookbook.id, 2)
        self.assertEqual(cookbook.name, "changed_name")
        self.assertEqual(cookbook.notes, "Okay")

    def test_from_values(self):
        values = ["123", "Harry Potter Cookbook", "Magical"]
        cookbook = Cookbook.from_values(values)
        self.assertEqual(cookbook.id, 123)
        self.assertEqual(cookbook.name, "Harry Potter Cookbook")
        self.assertEqual(cookbook.notes, "Magical")

    def test_to_tuple(self):
        cookbook = Cookbook(123, "Harry Potter Cookbook", "Magical")
        self.assertEqual(cookbook.to_tuple(), (123, "Harry Potter Cookbook", "Magical"))


if __name__ == '__main__':
    unittest.main()
