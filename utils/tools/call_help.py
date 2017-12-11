# -*- coding: utf-8 -*-

import sys

import config as conf


def baseHelp(exit_code=0, is_exit=True):
    print('python manager.py [OPTION]')
    if is_exit:
        sys.exit(exit_code)


def resultHelp(exit_code=0):
    baseHelp(exit_code, is_exit=False)
    print('option result [OPTION]')
    sys.exit(exit_code)


def historyHelp(exit_code=0):
    baseHelp(exit_code, is_exit=False)
    print('option history [OPTION]')
    sys.exit(exit_code)
