# !/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from utils.reader import (
    readLog,
    readDataDir,
    readLastData,
)
from utils.stock import train
from config import TEST_RESULT_WIDTH


class TestReader(unittest.TestCase):
    def test_reader_file(self):
        test_len = 30
        result_len = 5
        i = 0
        for test, result in readLog("0600287.log", test_len, result_len):
            if i == 0:
                print(test, result)
                self.assertEqual(len(test), test_len)
                # for row in test:
                #     print(row)
                # print(result)
                self.assertEqual(len(result), result_len)

                self.assertNotEqual(float(result[2]), 0)

            i += 1
        print(i)

        readLine = 30
        predictions = readLastData("0600287.log", readLine)
        self.assertEqual(len(predictions), readLine)

    def test_reader_dir(self):
        file_n = 0
        for _log in readDataDir():
            self.assertRegexpMatches(_log, r'^[0-9]+\.log$')
            file_n += 1
        print("There are %s stock log" % file_n)

    def test_stock_batch(self):
        batch_train = train.next_batch(50)
        # print(type(batch_train.__next__()))
        i = 0
        for _train, _test in batch_train:
            print(i)
            i += 1
            self.assertEqual(50, len(_train))
            print(_test)
            self.assertEqual(TEST_RESULT_WIDTH, len(_test[0]))
            break


if __name__ == '__main__':
    unittest.main()
