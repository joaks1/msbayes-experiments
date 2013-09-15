#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def main_cli():
    info_path = os.path.join(project_util.RESULT_DIR, 'old',
                'pymsbayes-results', 'pymsbayes-info.txt')
    _LOG.info('Parsing and writing results...')
    results = DMCSimulationResults(info_path)
    prior_indices = results.prior_index_to_config.keys()
    results.write_result_summaries(
            prior_indices = prior_indices,
            include_tau_exclusion_info = False)

if __name__ == '__main__':
    main_cli()

