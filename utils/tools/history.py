# -*- coding: utf-8 -*-

import os
import sys
# import time
import getopt
import requests
from datetime import date

import config as conf
from utils.tools.call_help import historyHelp

access_url = "http://quotes.money.163.com/service/chddata.html"


def getStockCodes(loadstatus):
    if loadstatus == 'all':
        code_list = []
        code_file = os.path.join(os.getcwd(), conf.STOCK_CODE_LIST)
        with open(code_file, 'r') as code_f:
            code_list.append(code_f.read())
        return code_list
    else:
        return loadstatus.split(',')


def loadHistory(start_t, end_t, codes=[]):
    print("load history train data", codes)

    for code in codes:
        params = {"code": code,
                  "start": start_t,
                  "end": end_t,
                  "fields": "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"}

        response = requests.get(access_url, params, stream=True)
        print("stock(%s) load status(%s)" % (code, response.status_code))

        if response.status_code != 200:
            continue
        context = response.content.decode('gbk')
        if len(context.splitlines()) == 1:
            continue

        save_path = os.path.join(os.getcwd(), conf.STOCK_HISTORY_DIR, code)
        with open(save_path, 'w') as h_f:
            h_f.write(context)


def findStockCode():
    save_path = os.path.join(os.getcwd(), conf.STOCK_CODE_LIST)
    with open(save_path, 'w') as code_f:
        end_t = date.today()
        start_t = date(end_t.year, end_t.month, end_t.day-2)
        _end = end_t.strftime("%Y%m%d")
        _start = start_t.strftime("%Y%m%d")
        params = {"start": _start,
                  "end": _end,
                  "fields": "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"}
        for code in range(1, 10000):
            for prefix in ['06', '10', '13']:
                if code % 100 == 0:
                    sys.stdout.write(".")

                stock_k = str(code).zfill(5)
                params['code'] = prefix + stock_k
                response = requests.get(access_url, params, timeout=1)

                if response.status_code != 200:
                    continue
                context = response.content.decode('gbk')
                if len(context.splitlines()) == 1:
                    continue
                code_f.write(params['code'] + "\n")
                print(params)


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "hfl:s:e:")
    except getopt.GetoptError as e:
        print(e)
        historyHelp(2)

    args = {}
    today = date.today()
    args['end_t'] = today.strftime("%Y%m%d")
    startDay = date(today.year-conf.STOCK_HISTORY_YEAR,
                    today.month,
                    today.day)
    args['start_t'] = startDay.strftime("%Y%m%d")
    for opt, arg in opts:
        if opt == '-h':
            historyHelp()
        elif opt == '-s':
            args['start_t'] = arg
        elif opt == '-e':
            args['end_t'] = arg
        elif opt == '-l':
            args['codes'] = getStockCodes(arg)
        elif opt == '-f':
            print("search all stock code")
            findStockCode()

    print(args)
    if "codes" in args:
        loadHistory(**args)
    else:
        historyHelp()
