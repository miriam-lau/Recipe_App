import unittest
from entities.cookbook_manager import CookbookManager
from entities.cookbook import Cookbook



class TestCookbookManager(unittest.TestCase):

    def test_create_and_initialize_cookbook_manager(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbooks = cookbook_manager.get_cookbooks()
        self.assertEqual(len(cookbooks), 2)
        self.assertEqual(cookbooks[0], Cookbook(4, "Joy of Cooking"))
        self.assertEqual(cookbooks[1], Cookbook(2, "Momofuku"))

    def test_add_cookbook(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "Atelier Crenn"), "testing/test_add_cookbook.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "Smitten Kitchen"), "testing/test_add_cookbook.txt")
        cookbook_manager.add_new_cookbook(Cookbook(None, "America's Test Kitchen"), "testing/test_add_cookbook.txt")
        cookbooks = cookbook_manager.get_cookbooks()

        self.assertEqual(len(cookbooks), 5)
        self.assertEqual(cookbooks[0], Cookbook(5, "America's Test Kitchen"))
        self.assertEqual(cookbooks[1], Cookbook(1, "Atelier Crenn"))
        self.assertEqual(cookbooks[2], Cookbook(4, "Joy of Cooking"))
        self.assertEqual(cookbooks[3], Cookbook(2, "Momofuku"))
        self.assertEqual(cookbooks[4], Cookbook(3, "Smitten Kitchen"))

    def test_get_cookbook(self):
        cookbook_manager = CookbookManager.create_and_initialize_cookbook_manager("testing/cookbooks.txt")
        cookbook = cookbook_manager.get_cookbook(2)
        self.assertEqual(cookbook, Cookbook(2, "Momofuku"))


if __name__ == '__main__':
    unittest.main()
