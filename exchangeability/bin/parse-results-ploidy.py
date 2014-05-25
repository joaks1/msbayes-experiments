#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.utils.messaging import get_logger

_LOG = get_logger(__name__)

def main_cli():
    bin_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.abspath(os.path.dirname(bin_dir))
    result_dir = os.path.abspath(os.path.join(project_dir, 'results'))
    info_path = os.path.join(result_dir, 'ploidy-sort', 'pymsbayes-results',
            'pymsbayes-info.txt')
    _LOG.info('Parsing and writing results...')
    results = DMCSimulationResults(info_path)
    prior_indices = results.prior_index_to_config.keys()
    results.write_result_summaries(
            prior_indices = prior_indices,
            include_tau_exclusion_info = False)

if __name__ == '__main__':
    main_cli()

