#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import (DMCSimulationResults,
        get_dict_from_spreadsheets)
from pymsbayes.fileio import process_file_arg, expand_path
from pymsbayes.utils.stats import mode_list, median
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def summarize_sim_results(info_path):
    info_path = expand_path(info_path)
    sim_results = DMCSimulationResults(info_path)
    out_dir = os.path.dirname(info_path)
    summary_path = os.path.join(out_dir, 'results-summary.txt')
    result_path = sim_results.get_result_summary_path(observed_index = 1,
            prior_index = sim_results.combined_prior_index)
    d = get_dict_from_spreadsheets([result_path])
    num_excluded = [int(x) for x in d['num_excluded']]
    num_excluded_glm = [int(x) for x in d['num_excluded_glm']]
    prob_of_exclusion = [float(x) for x in d['prob_of_exclusion']]
    prob_of_exclusion_glm = [float(x) for x in d['prob_of_exclusion_glm']]
    num_sims = sum_results.num_sim_reps
    assert len(num_excluded) == num_sims
    assert len(num_excluded_glm) == num_sims
    assert len(prob_of_exclusion) == num_sims
    assert len(prob_of_exclusion_glm) == num_sims
    summary_stream, close = process_file_arg(summary_path, 'w')
    summary_stream.write('Proportion of simulations excluding truth: {0}'
            '\n'.format(
                len([1 for x in num_excluded if x > 0]) / float(num_sims)))
    summary_stream.write('Proportion of simulations excluding truth with GLM-'
            'adjustment: {0}\n'.format(
                len([1 for x in num_excluded_glm if x > 0]) / float(num_sims)))
    summary_stream.write('Average number of tau parameters excluded: {0}'
            '\n'.format(
                sum(num_excluded) / float(num_sims)))
    summary_stream.write('Average number of tau parameters excluded with GLM: '
            '{0}\n'.format(sum(num_excluded_glm) / float(num_sims)))
    summary_stream.write('Mode number of tau parameters excluded: {0}\n'.format(
            mode_list(num_excluded)))
    summary_stream.write('Mode number of tau parameters excluded with GLM: '
            '{0}\n'.format(mode_list(num_excluded_glm)))
    summary_stream.write('Max number of tau parameters excluded: {0}\n'.format(
            max(num_excluded)))
    summary_stream.write('Max number of tau parameters excluded with GLM: '
            '{0}\n'.format(max(num_excluded_glm)))
    summary_stream.write('Average probability of exclusion: {0}\n'.format(
            sum(prob_of_exclusion) / float(num_sims)))
    summary_stream.write('Average probability of exclusion with GLM: {0}\n'.format(
            sum(prob_of_exclusion_glm) / float(num_sims)))
    summary_stream.write('Median probability of exclusion: {0}\n'.format(
            median(prob_of_exclusion)))
    summary_stream.write('Median probability of exclusion with GLM: {0}\n'.format(
            median(prob_of_exclusion_glm)))
    summary_stream.close()

def main_cli():
    for sim_dir in ['m1-01-sim', 'm1-1-sim']:
        sim_info_path = os.path.join(project_util.RESULT_DIR, sim_dir,
                'pymsbayes-results', 'pymsbayes-info.txt')
        summarize_sim_results(sim_info_path)

if __name__ == '__main__':
    main_cli()

