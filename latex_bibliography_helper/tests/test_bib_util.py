import unittest

try:
    # When executed within PyCharm
    import latex_bibliography_helper.bib_util as bib_util
except ImportError:
    # When executed in the root directory as:
    # pyton -m unittest tests.test_bib_util
    import bib_util

import bibtexparser


class TestCurlify(unittest.TestCase):

    def _prepare_bib(self, title):
        bib_content = """
@article{TestPlaceholder,
    author        = {Max Mustermann and
                   Lisa Mueller and
                   Maxime Test},
    title         = {""" + title + """},
    journal       = {CoRR},
    year          = {2021},
}
        """
        # Title is already wrapped into {}
        # E.g. Title = "Hello World!"
        # Result will be: {Hello World!}
        bib = bibtexparser.loads(bib_content)
        return bib.entries[0]

    def _curlify(self, bib_entry) -> str:
        bib_util.curlify_title(bib_entry)
        return bib_entry["title"]

    def test_do_nothing(self):
        bib_entry = self._prepare_bib("{Hello}")
        result = self._curlify(bib_entry)
        self.assertEqual("{Hello}", result)

    def test_add_curly(self):
        bib_entry = self._prepare_bib("Hello")
        result = self._curlify(bib_entry)
        self.assertEqual("{Hello}", result)

    def test_do_nothing_long(self):
        bib_entry = self._prepare_bib("{Hello {WORLD} - {P}ython is {great}}")
        result = self._curlify(bib_entry)
        self.assertEqual("{Hello {WORLD} - {P}ython is {great}}", result)

    def test_add_curly_long(self):
        bib_entry = self._prepare_bib("Hello {WORLD} - {P}ython is {great}")
        result = self._curlify(bib_entry)
        self.assertEqual("{Hello {WORLD} - {P}ython is {great}}", result)


if __name__ == '__main__':
    unittest.main()
