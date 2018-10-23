import unittest
from entities.cookbook import Cookbook


class TestCookbook(unittest.TestCase):

    def test_setters(self):
        cookbook = Cookbook(1, "default")
        cookbook.name = "changed_name"
        cookbook.id = 2
        self.assertEqual(cookbook.id, 2)
        self.assertEqual(cookbook.name, "changed_name")

    def test_from_line(self):
        line = "123,Harry Potter Cookbook\n"
        cookbook = Cookbook.from_line(line)
        self.assertEqual(cookbook.id, 123)
        self.assertEqual(cookbook.name, "Harry Potter Cookbook")

    def test_to_line(self):
        cookbook = Cookbook(123, "Harry Potter Cookbook")
        self.assertEqual(cookbook.to_line(), "123,Harry Potter Cookbook\n")


if __name__ == '__main__':
    unittest.main()
