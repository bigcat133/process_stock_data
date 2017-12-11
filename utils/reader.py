#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv
import numpy as np

from config import (
    STOCK_DATA_PATH,
    TEST_COLUMN_LIST,
    TYPE_CONF_DIR,
    READ_TEST_DAY,
)


def readDataDir(train_name=None):
    select_list = []
    if train_name:
        _conf_dir = os.path.join(os.getcwd(), TYPE_CONF_DIR)
        with open(os.path.join(_conf_dir, train_name), 'r') as train_logs_f:
            for stock_code in train_logs_f:
                select_list.append(stock_code.strip())

    for f in os.listdir(STOCK_DATA_PATH):
        if select_list and f.split(".")[0] not in select_list:
            continue
        f_path = os.path.join(STOCK_DATA_PATH, f)
        if os.path.isfile(f_path) and re.match(r"^\d+\.log$", f):
            yield f


def initRow(org_data, init_row):
    for i in range(len(org_data)):
        row = org_data[i]
        if row[5] == 'None':
            org_data[i] = init_row
        else:
            init_row = row
    return org_data


def _readAllData(fileN, readLine=None):
    _trainsList = []
    with open(os.path.join(STOCK_DATA_PATH, fileN)) as csvfile:
        _stock = csv.reader(csvfile, delimiter=",", quotechar=',')
        try:
            _stock.__next__()
        except UnicodeDecodeError as ex:
            raise ex

        for row in _stock:
            if isinstance(readLine, int):
                if readLine <= 0:
                    break
                else:
                    readLine -= 1

            _tmp_row = []
            for i in range(len(row)):
                if i in TEST_COLUMN_LIST:
                    try:
                        _tmp_row.append(float(row[i]))
                    except:
                        _tmp_row.append("None")
            _trainsList.append(_tmp_row)

    return _trainsList


def readLog(fileN, test_len, result_len, step=5):
    """
    fileN, read stock log file name
    r_len, read data len of to predict
    s_len, result data len
    """

    trainsList = _readAllData(fileN)

    # trainsList.reverse()

    _cursor = len(trainsList) - 1
    _init_row = None
    _test = []
    _tmp = []
    _test_len = _result_len = 0
    while (_cursor - _test_len - _result_len) >= 0:
        # print(fileN, _cursor, _test_len, _result_len, test_len, result_len)
        _tmp_r = trainsList[_cursor - _test_len - _result_len]
        if _tmp_r[5] == "None":
            if _init_row:
                _tmp_r = _init_row
            else:
                _cursor -= 1
                continue
        else:
            _init_row = _tmp_r

        if _test_len < test_len:
            _test.append(_tmp_r)
            _test_len += 1
            continue

        if _result_len < result_len:
            _tmp.append(_tmp_r)
            _result_len += 1
            continue

        # set read test row and result row again
        _test_len = _result_len = 0

        _result = [i[0] for i in _tmp]
        _cursor -= step
        # print(fileN, _cursor)
        yield _test, _result
        _test = _result = []


def readLastData(fileN, readLine=None):
    if not readLine:
        readLine = READ_TEST_DAY
    dataList = _readAllData(fileN, readLine)

    # return np.concatenate(dataList)
    return (dataList,)
