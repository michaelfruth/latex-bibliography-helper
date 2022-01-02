import unittest

try:
    # When executed within PyCharm
    import latex_bibliography_helper.bibtex_handler as bibtex_handler
except ImportError:
    # When executed in the root directory as:
    # pyton -m unittest tests.test_latex_handler
    import bibtex_handler


class TestCreateAttributeOrder(unittest.TestCase):

    def _check(self, expected, result):
        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i], result[i])

    def test_simple_single(self):
        current_attributes = ["a", "b", "c"]
        plain_attributes_order = ["b"]
        expected = ["b"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_simple_multi(self):
        current_attributes = ["a", "b", "c"]
        plain_attributes_order = ["b", "a"]
        expected = ["b", "a"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_simple_all(self):
        current_attributes = ["a", "b", "c"]
        plain_attributes_order = ["b", "a", "c"]
        expected = ["b", "a", "c"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_no_match(self):
        current_attributes = ["a", "b", "c"]
        plain_attributes_order = ["x", "y", "z"]
        expected = []
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_part_match(self):
        current_attributes = ["a", "b", "c", "m"]
        plain_attributes_order = ["x", "y", "m", "z"]
        expected = ["m"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_prefix_1(self):
        current_attributes = ["a", "b", "c", "_a", "_c"]
        plain_attributes_order = ["c", "b"]
        expected = ["c", "_c", "b"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_prefix_2(self):
        current_attributes = ["__a", "a", "___a", "b", "__aa", "c", "_a", "_c"]
        plain_attributes_order = ["a"]
        expected = ["a", "_a", "__a", "___a"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

    def test_prefix_3(self):
        current_attributes = ["__a", "a", "___a", "b", "__aa", "c", "_a", "_c"]
        plain_attributes_order = ["b", "c", "a"]
        expected = ["b", "c", "_c", "a", "_a", "__a", "___a"]
        result = bibtex_handler.create_attributes_order(current_attributes, plain_attributes_order, "_")
        self._check(expected, result)

