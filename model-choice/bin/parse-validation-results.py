#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

VALIDATION_INFO_PATH = os.path.join(project_util.RESULT_DIR, 'validation',
        'results', 'pymsbayes-results', 'pymsbayes-info.txt')

def _check_path():
    print os.path.exists(VALIDATION_INFO_PATH)
    with open(VALIDATION_INFO_PATH, 'rU') as f:
        print f.read()

def main_cli():
    _LOG.info('Parsing and writing results...')
    v_results = DMCSimulationResults(VALIDATION_INFO_PATH)
    v_results.write_result_summaries(
            prior_indices = [v_results.combined_prior_index],
            include_tau_exclusion_info = True)

if __name__ == '__main__':
    # _check_path()
    main_cli()

