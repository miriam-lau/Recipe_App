import unittest
from .cookbook_manager import CookbookManager
from .cookbook import Cookbook



class TestCookbookManager(unittest.TestCase):

    def test_create_and_initialize_cookbook_manager(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbooks = cookbook_manager.get_cookbooks()
        self.assertEqual(len(cookbooks), 2)
        self.assertEqual(cookbooks[0], Cookbook(7, "Joy of Cooking", "Great"))
        self.assertEqual(cookbooks[1], Cookbook(6, "Momofuku", "Okay"))

    def test_add_cookbook(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "Atelier Crenn", "Superb"), "testing/test_add_cookbook.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "Smitten Kitchen", "Meh"), "testing/test_add_cookbook.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "America's Test Kitchen", "Bad"), \
                                          "testing/test_add_cookbook.txt")
        cookbooks = cookbook_manager.get_cookbooks()

        self.assertEqual(len(cookbooks), 5)
        self.assertEqual(cookbooks[0], Cookbook(3, "America's Test Kitchen", "Bad"))
        self.assertEqual(cookbooks[1], Cookbook(1, "Atelier Crenn", "Superb"))
        self.assertEqual(cookbooks[2], Cookbook(7, "Joy of Cooking", "Great"))
        self.assertEqual(cookbooks[3], Cookbook(6, "Momofuku", "Okay"))
        self.assertEqual(cookbooks[4], Cookbook(2, "Smitten Kitchen", "Meh"))

    def test_get_cookbook(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbook = cookbook_manager.get_cookbook(6)
        self.assertEqual(cookbook, Cookbook(6, "Momofuku", "Okay"))


if __name__ == '__main__':
    unittest.main()
