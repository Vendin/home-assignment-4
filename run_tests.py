# -*- coding: utf-8 -*-

import unittest
from test import test
import sys

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(test.TargetTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
