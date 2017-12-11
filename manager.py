# -*- coding: utf-8 -*-

import sys
import importlib

from utils.tools.call_help import baseHelp


def main(argv):
    if len(argv) < 2:
        baseHelp()

    argv = argv[1:]
    worker_name = argv[0]

    try:
        _run_model = importlib.import_module("utils.tools." + worker_name)
        _run_model.run(argv[1:])
    except Exception as ex:
        raise ex
        baseHelp(1)


if __name__ == "__main__":
    main(sys.argv)
