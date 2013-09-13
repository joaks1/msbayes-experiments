#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def main_cli():
    info_path = os.path.join(project_util.RESULT_DIR,
                'pymsbayes-results', 'pymsbayes-info.txt')
    _LOG.info('Parsing and writing results...')
    power_results = DMCSimulationResults(info_path)
    prior_indices = power_results.prior_index_to_config.keys()
    print prior_indices
    # power_results.write_result_summaries(
    #         prior_indices = [power_results.combined_prior_index],
    #         include_tau_exclusion_info = True)

if __name__ == '__main__':
    main_cli()

