#!/usr/bin/env python

import unittest

import dejumble.filters.null
from dejumble.filters.null import *

class NullFileListFilterTestCase(unittest.TestCase):
    def testfilelist(self):
        filelist = list(NullFileListFilter().filelist())
        self.assertEqual(len(filelist), 1)
        self.assertEqual(filelist[0], '/dev/null')
