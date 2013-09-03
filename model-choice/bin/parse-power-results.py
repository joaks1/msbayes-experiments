#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import (DMCSimulationResults,
        parse_posterior_summary_file, dict_line_iter)
from pymsbayes.config import MsBayesConfig
from pymsbayes.utils.stats import mode_list
from pymsbayes.utils.fileio import process_file_arg
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

POWER_INFO_PATH = os.path.join(project_util.RESULT_DIR, 'power',
        'pymsbayes-results', 'pymsbayes-info.txt')

def main_cli():
    _LOG.info('Parsing and writing results...')
    power_results = DMCSimulationResults(POWER_INFO_PATH)
    power_results.write_result_summaries(
            prior_indices = [power_results.combined_prior_index],
            compress = True)

if __name__ == '__main__':
    main_cli()

