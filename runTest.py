#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from tests.testReader import TestReader


def test_reader():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestReader)
    test_suite_result = unittest.TestResult()
    test_suite.run(test_suite_result)
    for err in test_suite_result.errors:
        print("err", err)
    for fail in test_suite_result.failures:
        print("fail", fail)


def test_run():
    pass


if __name__ == "__main__":
    test_reader()
