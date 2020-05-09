import unit_helper
import unittest
import re, os, sys

from unit_helper import *

class HttperfTestCase(unittest.TestCase):

    def testParse(self):
        global presults
        presults = HttperfParser().parse(httperf_results)

    def testParsedResult(self):
        self.assertEqual(presults, httperf_results_parsed)

    def testParsedHeaders(self):
        # the first header in httperf_headers_results has a 0 sample
        # flag so it should not appear in the results.
        presults = HttperfParser().parse(httperf_headers_results)
        self.assertEqual(presults, httperf_headers_parsed)

    @unittest.skip('not using kmervine/httperfpy')
    def testParseVerboseResultCount(self):
        vpresults = HttperfParser().parse(httperf_verbose_results)
        self.assertEqual(len(vpresults.keys()), 57)
        self.assertEqual(len(vpresults["connection_times"]), 10)

if __name__ == "__main__":
    unittest.main()

