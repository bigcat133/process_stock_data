#! /usr/bin/python
# -*- coding: utf-8 -*-

# original stock data path
STOCK_DATA_PATH = "/data/stock/stock/history/price"

# first process data path, there are the process source
PROCESS_DATA_PATH = "/data/stock/stock/history/result/"

# read test column number
TEST_COLUMN_LIST = (3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14)

# read stock data config
READ_TEST_DAY = 60
READ_TEST_WIDTH = len(TEST_COLUMN_LIST)
READ_RESULT_DAY = 3
READ_NEXT_STEP = 5
READ_LOG_LONG = 99    # the train batch data long

# test result prop
TEST_RESULT_PROP = [-9, -4, 0, 4, 9]
# TEST_RESULT_PROP = [-8, 8]
# TEST_RESULT_PROP = [0]
TEST_RESULT_WIDTH = len(TEST_RESULT_PROP) + 1

# filter out test data ratio
TEST_RATIO = 50
SHOW_READ_STOCK_NAME = False

# define read stock file config
TYPE_CONF_DIR = 'stock_config/type_conf'
MODEL_SAVE_PATH = "stock_config/sess_model"
RESULT_SAVE_PATH = "stock_config/result"

# cache stock flag
CACHE_STOCK_DATA = False

# stock history config
STOCK_CODE_LIST = 'stock_config/stock_codes.info'
STOCK_HISTORY_DIR = 'stock_config/history'
STOCK_HISTORY_YEAR = 8
