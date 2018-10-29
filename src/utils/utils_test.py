import unittest
from .utils import compare


class TestUtils(unittest.TestCase):

    def test_compare(self):
        self.assertEqual(compare(0.1, 0.1), 0)
        self.assertEqual(compare(0.1, 0.2), -1)
        self.assertEqual(compare(0.2, 0.1), 1)


if __name__ == '__main__':
    unittest.main()
