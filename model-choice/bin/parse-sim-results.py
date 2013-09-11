#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults
from pymsbayes.fileio import expand_path
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def parse_sim_results(info_path):
    _LOG.info('Parsing and writing results...')
    info_path = expand_path(info_path)
    sim_results = DMCSimulationResults(info_path)
    sim_results.write_result_summaries(
            prior_indices = [sim_results.combined_prior_index],
            include_tau_exclusion_info = True)

def main_cli():
    for sim_dir in ['m1-01-sim', 'm1-1-sim']:
        sim_info_path = os.path.join(project_util.RESULT_DIR, sim_dir,
                'pymsbayes-results', 'pymsbayes-info.txt')
        parse_sim_results(sim_info_path)

if __name__ == '__main__':
    main_cli()

