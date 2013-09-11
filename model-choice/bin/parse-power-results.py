#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

POWER_INFO_PATHS = [
        os.path.join(project_util.RESULT_DIR, 'power',
                'pymsbayes-results', 'pymsbayes-info.txt'),
        os.path.join(project_util.RESULT_DIR, 'power-1',
                'pymsbayes-results', 'pymsbayes-info.txt')]

def main_cli():
    _LOG.info('Parsing and writing results...')
    for info_path in POWER_INFO_PATHS:
        power_results = DMCSimulationResults(info_path)
        power_results.write_result_summaries(
                prior_indices = [power_results.combined_prior_index])

if __name__ == '__main__':
    main_cli()

