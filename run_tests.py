# -*- coding: utf-8 -*-

import unittest
from test import profile_test
from test import audience_test
import sys

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(profile_test.TargetTestProfile),
        # unittest.makeSuite(audience_test.TargetTestAudience),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
