import unittest

try:
    # When executed within PyCharm
    import bibhelper.handler.latex_handler as latex_handler
except ImportError:
    # When executed in the root directory as:
    # pyton -m unittest tests.test_latex_handler
    import handler.latex_handler


class TestBooktitle(unittest.TestCase):

    def test_many(self):
        booktitles = [
            ("ISCA",
             "43rd {ACM/IEEE} Annual International Symposium on Computer Architecture, {ISCA} 2016, Seoul, South Korea, June 18-22, 2016"),
            ("OOPSLA",
             "Proceedings of the 22nd Annual {ACM} {SIGPLAN} Conference on Object-Oriented Programming, Systems, Languages, and Applications, {OOPSLA} 2007, October 21-25, 2007, Montreal, Quebec, Canada"),
            (None,
             "Proceedings of the 12th International Workshop on Data Management on New Hardware"),
            ("ICDE",
             "36th {IEEE} International Conference on Data Engineering, {ICDE} 2020, Dallas, TX, USA, April 20-24, 2020"),
            ("DaMoN",
             "Proceedings of the 12th International Workshop on Data Management on New Hardware, DaMoN 2016, San Francisco, CA, USA, June 27, 2016}"),
            (None,
             "9th Workshop on Systems for Multi-core and Heterogenous Architectures"),
            ("CIDR",
             "Sixth Biennial Conference on Innovative Data Systems Research, {CIDR} 2013, Asilomar, CA, USA, January 6-9, 2013, Online Proceedings"),
            ("EuroSys",
             "EuroSys '21: Sixteenth European Conference on Computer Systems, Online Event, United Kingdom, April 26-28, 202"),
            ("SoCC",
             "Proceedings of the 1st {ACM} Symposium on Cloud Computing, SoCC 2010, Indianapolis, Indiana, USA, June 10-11, 2010"),
            (None,
             "Encyclopedia of Big Data Technologies"),
            ("PACT", "{PACT} '20: International Conference on Parallel Architectures and Compilation Techniques")
        ]
        for expected, booktitle in booktitles:
            shortname = latex_handler.extract_booktitle_shortname(booktitle)
            self.assertEqual(expected, shortname)

    def test_shortname_year_single(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "2016 {IEEE} International Symposium on Workload Characterization, {IISWC} 2016, Providence, RI, USA, September 25-27, 2016")
        self.assertEqual("IISWC", shortname)

    def test_shortname_year_multi(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "2016 {IEEE} International Symposium on Workload Characterization, {IISWC}\n"
            "2016, Providence, RI, USA, September 25-27, 2016")
        self.assertEqual("IISWC", shortname)

    def test_shortname_end_single(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "2014 IEEE International Symposium on Workload Characterization {IISWC}")
        self.assertEqual("IISWC", shortname)

    def test_shortname_end_multi(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "2014 IEEE International Symposium\n"
            "on Workload Characterization\n"
            "{IISWC}")
        self.assertEqual("IISWC", shortname)

    def shortname_start_single(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "EuroSys '21: Sixteenth European Conference on Computer Systems, Online Event, United Kingdom, April 26-28, 202")
        self.assertEqual("EuroSys", shortname)

    def shortname_start_mutli(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "EuroSys\n"
            "'21: Sixteenth European Conference\n"
            "on Computer Systems, Online Event,\n"
            "United Kingdom, April 26-28, 202")
        self.assertEqual("EuroSys", shortname)

    def shortname_none_single(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "Encyclopedia of Big Data Technologies")
        self.assertEqual(None, shortname)

    def shortname_none_multi(self):
        shortname = latex_handler.extract_booktitle_shortname(
            "Encyclopedia\n"
            "of Big Data\n"
            "Technologies")
        self.assertEqual(None, shortname)


class TestCurlify(unittest.TestCase):

    def test_do_nothing(self):
        result = latex_handler.curlify("{Hello}")
        self.assertEqual("{Hello}", result)

    def test_add_curly(self):
        result = latex_handler.curlify("Hello")
        self.assertEqual("{Hello}", result)

    def test_do_nothing_long(self):
        result = latex_handler.curlify("{Hello {WORLD} - {P}ython is {great}}")
        self.assertEqual("{Hello {WORLD} - {P}ython is {great}}", result)

    def test_add_curly_long(self):
        result = latex_handler.curlify("Hello {WORLD} - {P}ython is {great}")
        self.assertEqual("{Hello {WORLD} - {P}ython is {great}}", result)

    def test_odd_curly_bracket_left(self):
        result = latex_handler.curlify("{Hello")
        self.assertEqual("{{Hello}", result)

    def test_odd_curly_bracket_right(self):
        result = latex_handler.curlify("Hello}")
        self.assertEqual("{Hello}}", result)

    def test_odd_curly_bracket_long(self):
        result = latex_handler.curlify("{{Hello} WORLD} {HI} {{{HI } Python} 3")
        self.assertEqual("{{{Hello} WORLD} {HI} {{{HI } Python} 3}", result)


if __name__ == '__main__':
    unittest.main()
