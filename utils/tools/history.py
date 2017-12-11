# -*- coding: utf-8 -*-

import os
# import sys
import getopt
# import yaml
import json

import config as conf
from utils.tools.call_help import historyHelp


def createHistory():
    print("create new history train data")
    pass


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "hn")
    except getopt.GetoptError as e:
        print(e)
        historyHelp(2)

    for opt, arg in opts:
        if opt == '-h':
            historyHelp()
        elif opt == '-n':
            return createHistory()

    historyHelp()
