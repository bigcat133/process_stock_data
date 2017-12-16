# -*- coding: utf-8 -*-

import os
import sys
import getopt
import importlib
# import argparse

import config as conf
from utils.tools.call_help import trainHelp


def runTrain(run_model, argv):
    try:
        print("##########################")
        print("## Start %s train" % run_model)
        print("##########################")
        pid = os.fork()
        if pid == 0:
            _run_model = importlib.import_module("lib.train." + run_model)
            accur = _run_model.run(**argv)
            print("%s Testing Accuracy %s" % (run_model, accur))
            sys.exit(0)
        else:
            os.waitpid(pid, 0)
    except Exception as ex:
        raise ex
        trainHelp(1)


def runSomeTrain(run_model, argv, trainList):
    for fileN in trainList.split(','):
        fileN = fileN.strip()
        if fileN == "format.sh":
            continue
        print(fileN)
        argv["train_name"] = fileN
        argv["save_name"] = fileN
        runTrain(run_model, argv)


def runAllTrain(run_model, argv):
    trainConfDir = os.path.join(os.getcwd(), conf.TYPE_CONF_DIR)
    for fileN in os.listdir(trainConfDir):
        if fileN == "format.sh":
            continue
        print(fileN)
        argv["train_name"] = fileN
        argv["save_name"] = fileN
        runTrain(run_model, argv)


def run(argv):
    global CACHE_STOCK_DATA
    run_model = 'rnn'
    _argv = {}
    train_name = None
    try:
        opts, args = getopt.getopt(argv, "hmt:c:n:s:")
    except getopt.GetoptError as e:
        print(e)
        trainHelp(2)

    for opt, arg in opts:
        if opt == '-h':
            trainHelp()
        elif opt in ("-t"):
            run_model = arg
        elif opt in ("-c"):
            train_name = arg
        elif opt in ("-n"):
            _argv["train_num"] = int(arg)
        elif opt == '-m':
            conf.CACHE_STOCK_DATA = True
        elif opt == '-s' and arg:
            _argv["save_name"] = arg

    if train_name is None:
        trainHelp()

    if train_name == "all":
        runAllTrain(run_model, _argv)
    else:
        runSomeTrain(run_model, _argv, train_name)
