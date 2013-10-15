#! /usr/bin/env python

import os
import sys
import glob

BIN_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.dirname(BIN_DIR))
PLOT_DIR = os.path.join(PROJECT_DIR, 'plots')
CONFIG_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'configs'))
RESULTS_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'results'))
PHILIPPINES_DIR = os.path.abspath(os.path.join(RESULTS_DIR, 'philippines'))
PHILIPPINES_DPP_DIR = os.path.abspath(os.path.join(PHILIPPINES_DIR, 'dpp'))
PHILIPPINES_DPP_INFO = os.path.join(PHILIPPINES_DPP_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')


def main():
    sys.stdout.write("%s" % PROJECT_DIR)

if __name__ == '__main__':
    main()

