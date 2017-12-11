# -*- coding: utf-8 -*-

import numpy as np

from utils.reader import (
    readDataDir,
    readLog,
)
from config import (
    READ_TEST_DAY,
    READ_RESULT_DAY,
    READ_NEXT_STEP,
    TEST_RESULT_PROP,
    TEST_RESULT_WIDTH,
    SHOW_READ_STOCK_NAME,
    TEST_RATIO,
    CACHE_STOCK_DATA,
)


class Train():
    def __init__(self, train_name=None):
        self.train_name = train_name
        self.init()

        if not CACHE_STOCK_DATA:
            self.clean()

        self.test_ratio = TEST_RATIO

        self.train_cache = {}
        self.test_cache = {'test': [], 'test_result': [], 'test_num': 0}

    def init(self):
        self.generator = readDataDir(self.train_name)
        self.train_num = 0
        self.train_result = []
        self.train = []

    def clean(self):
        self.init()

        self.train_cache = {}
        self.test_cache = {'test': [], 'test_result': [], 'test_num': 0}

    def _collect_train(self, train_data, result):
        last_price = float(train_data[len(train_data) - 1][0])

        sum_price = 0
        for _price in result:
            sum_price += float(_price)
        avg_price = sum_price / len(result)
        train_result = [0 for i in range(TEST_RESULT_WIDTH)]
        for inx in range(TEST_RESULT_WIDTH - 1):
            _test_price = last_price * (100 + TEST_RESULT_PROP[inx]) / 100
            if avg_price < _test_price:
                train_result[inx] = 1
                break
        else:
            train_result[len(TEST_RESULT_PROP)] = 1
        # print(train_result, )

        train_data = np.concatenate(train_data)
        if self.test_ratio == 0:
            self.test_cache['test'].append(train_data)
            self.test_cache['test_result'].append(train_result)
            self.test_cache['test_num'] += 1
            self.test_ratio = TEST_RATIO
        else:
            self.train.append(train_data)
            self.train_result.append(train_result)
            self.train_num += 1
            self.test_ratio -= 1

    def _pop_train(self):
        _train = self.train
        _train_result = self.train_result
        self.train = []
        self.train_result = []
        self.train_num = 0

        return _train, _train_result

    def next_batch(self, batch_n):
        for f in self.generator:
            if f in self.train_cache:
                for return_train in self.train_cache[f]:
                    yield return_train
                continue
            else:
                if SHOW_READ_STOCK_NAME:
                    print("not cache file:", f)

            if SHOW_READ_STOCK_NAME:
                print("####### read stock log : ", f, "######")
            for _train, _result in readLog(f,
                                           READ_TEST_DAY,
                                           READ_RESULT_DAY,
                                           READ_NEXT_STEP):
                self._collect_train(_train, _result)
                if self.train_num >= batch_n:
                    return_train = self._pop_train()
                    if CACHE_STOCK_DATA:
                        if f not in self.train_cache:
                            self.train_cache[f] = []
                        self.train_cache[f].append(return_train)
                    yield return_train

    def test_batch(self, batch_size=None):
        if not batch_size:
            print("return all test data")
            yield self.test_cache['test'], self.test_cache['test_result']
        else:
            print("return test data by yield")
            step = 0
            print("all test number: %s" % self.test_cache['test_num'])
            while step * batch_size < self.test_cache['test_num']:
                _cursor = step * batch_size
                _sub_t_cache = self.test_cache['test'][_cursor: _cursor + batch_size]
                _sub_t_result = self.test_cache['test_result'][_cursor:_cursor + batch_size]
                yield _sub_t_cache, _sub_t_result
                step += 1
                print("test step %s\n" % step)


train = Train()
