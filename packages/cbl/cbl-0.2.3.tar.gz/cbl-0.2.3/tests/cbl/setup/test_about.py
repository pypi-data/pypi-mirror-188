# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest

import cbl
from cbl.setup import about_package, about_platform, about_python


class SnippetInfoTestCase(unittest.TestCase):

    def test_about(self):
        about_pgk1 = cbl.setup.about_package()
        about_pgk2 = about_package()
        print(about_pgk1, about_pgk2)
        about_plt1 = cbl.setup.about_platform()
        about_plt2 = about_platform()
        print(about_plt1, about_plt2)
        about_python1 = cbl.setup.about_python()
        about_python2 = about_python()
        print(about_python1, about_python2)


if __name__ == '__main__':
    unittest.main()
