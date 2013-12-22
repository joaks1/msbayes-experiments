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
PHILIPPINES_DPP_SIMPLE_DIR = os.path.abspath(os.path.join(PHILIPPINES_DIR, 'dpp-simple'))
PHILIPPINES_DPP_INFORM_DIR = os.path.abspath(os.path.join(PHILIPPINES_DIR, 'dpp-inform'))
PHILIPPINES_UNIFORM_DIR = os.path.abspath(os.path.join(PHILIPPINES_DIR, 'uniform'))
PHILIPPINES_OLD_DIR = os.path.abspath(os.path.join(PHILIPPINES_DIR, 'old'))

PHILIPPINES_DPP_INFO = os.path.join(PHILIPPINES_DPP_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
PHILIPPINES_DPP_SIMPLE_INFO = os.path.join(PHILIPPINES_DPP_SIMPLE_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
PHILIPPINES_DPP_INFORM_INFO = os.path.join(PHILIPPINES_DPP_INFORM_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
PHILIPPINES_UNIFORM_INFO = os.path.join(PHILIPPINES_UNIFORM_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
PHILIPPINES_OLD_INFO = os.path.join(PHILIPPINES_OLD_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')

PHILIPPINES_DPP_CFG = os.path.join(CONFIG_DIR, 'philippines-dpp.cfg')
PHILIPPINES_DPP_SIMPLE_CFG = os.path.join(CONFIG_DIR, 'philippines-dpp-simple.cfg')
PHILIPPINES_DPP_INFORM_CFG = os.path.join(CONFIG_DIR, 'philippines-dpp-inform.cfg')
PHILIPPINES_UNIFORM_CFG = os.path.join(CONFIG_DIR, 'philippines-uniform.cfg')
PHILIPPINES_OLD_CFG = os.path.join(CONFIG_DIR, 'philippines-old.cfg')

NEGROS_PANAY_DIR = os.path.abspath(os.path.join(RESULTS_DIR, 'negros-panay'))
NP_DPP_ORDERED_DIR = os.path.abspath(os.path.join(NEGROS_PANAY_DIR, 'dpp-ordered'))
NP_DPP_ORDERED_INFO = os.path.join(NP_DPP_ORDERED_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
NP_DPP_UNORDERED_DIR = os.path.abspath(os.path.join(NEGROS_PANAY_DIR, 'dpp-unordered'))
NP_DPP_UNORDERED_INFO = os.path.join(NP_DPP_UNORDERED_DIR, 'pymsbayes-results', 'pymsbayes-info.txt')
NEGROS_PANAY_CFG = os.path.join(CONFIG_DIR, 'negros-panay.cfg')

def main():
    sys.stdout.write("%s" % PROJECT_DIR)

if __name__ == '__main__':
    main()

