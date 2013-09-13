#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import (DMCSimulationResults,
        get_dict_from_spreadsheets)
from pymsbayes.fileio import process_file_arg, expand_path
from pymsbayes.utils.stats import mode_list, median
from pymsbayes import plotting
from pymsbayes.config import MsBayesConfig
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
    bf_num_excluded = [int(x) for x in d['bf_num_excluded']]
    bf_num_excluded_glm = [int(x) for x in d['bf_num_excluded_glm']]
    prob_of_exclusion = [float(x) for x in d['prob_of_exclusion']]
    prob_of_exclusion_glm = [float(x) for x in d['prob_of_exclusion_glm']]
    prior_prob_of_exclusion = [float(x) for x in d['prior_prob_of_exclusion']]
    bf_of_exclusion = [float(x) for x in d['bf_of_exclusion']]
    bf_of_exclusion_glm = [float(x) for x in d['bf_of_exclusion_glm']]
    num_sims = sim_results.num_sim_reps
    assert len(num_excluded) == num_sims
    assert len(num_excluded_glm) == num_sims
    assert len(prob_of_exclusion) == num_sims
    assert len(prob_of_exclusion_glm) == num_sims
    summary_stream, close = process_file_arg(summary_path, 'w')
    summary_stream.write('Proportion of simulations excluding truth: {0}'
            '\n'.format(
                len([1 for x in bf_num_excluded if x > 0]) / float(num_sims)))
    summary_stream.write('Proportion of simulations excluding truth with GLM-'
            'adjustment: {0}\n'.format(
                len([1 for x in bf_num_excluded_glm if x > 0]) / float(num_sims)))
    summary_stream.write('Average number of tau parameters excluded: {0}'
            '\n'.format(
                sum(bf_num_excluded) / float(num_sims)))
    summary_stream.write('Average number of tau parameters excluded with GLM: '
            '{0}\n'.format(sum(bf_num_excluded_glm) / float(num_sims)))
    summary_stream.write('Mode number of tau parameters excluded: {0}\n'.format(
            mode_list(bf_num_excluded)))
    summary_stream.write('Mode number of tau parameters excluded with GLM: '
            '{0}\n'.format(mode_list(bf_num_excluded_glm)))
    summary_stream.write('Max number of tau parameters excluded: {0}\n'.format(
            max(bf_num_excluded)))
    summary_stream.write('Max number of tau parameters excluded with GLM: '
            '{0}\n'.format(max(bf_num_excluded_glm)))
    summary_stream.write('Average probability of exclusion: {0}\n'.format(
            sum(prob_of_exclusion) / float(num_sims)))
    summary_stream.write('Average probability of exclusion with GLM: {0}\n'.format(
            sum(prob_of_exclusion_glm) / float(num_sims)))
    summary_stream.write('Median probability of exclusion: {0}\n'.format(
            median(prob_of_exclusion)))
    summary_stream.write('Median probability of exclusion with GLM: {0}\n'.format(
            median(prob_of_exclusion_glm)))
    summary_stream.write('Average Bayes factor of exclusion: {0}\n'.format(
            sum(bf_of_exclusion) / float(num_sims)))
    summary_stream.write('Average Bayes factor of exclusion with GLM: {0}\n'.format(
            sum(bf_of_exclusion_glm) / float(num_sims)))
    summary_stream.write('Median Bayes factor of exclusion: {0}\n'.format(
            median(bf_of_exclusion)))
    summary_stream.write('Median Bayes factor of exclusion with GLM: {0}\n'.format(
            median(bf_of_exclusion_glm)))
    summary_stream.write('Max Bayes factor of exclusion: {0}\n'.format(
            max(bf_of_exclusion)))
    summary_stream.write('Max Bayes factor of exclusion with GLM: {0}\n'.format(
            max(bf_of_exclusion_glm)))
    prob_of_bf_exclusion = (len([1 for x in bf_of_exclusion if x > 10.0]) /
            float(num_sims))
    prob_of_bf_exclusion_glm = (len([
            1 for x in bf_of_exclusion_glm if x > 10.0]) /
            float(num_sims))
    summary_stream.write('Estimated probability Bayes factor of exclusion '
            '> 10: {0}\n'.format(prob_of_bf_exclusion))
    summary_stream.write('Estimated probability Bayes factor of exclusion '
            '> 10 with GLM: {0}\n'.format(prob_of_bf_exclusion_glm))
    summary_stream.close()
    if plotting.MATPLOTLIB_AVAILABLE:
        approx_prior_exclusion = 0.39184
        prior_odds = approx_prior_exclusion / (1.0 - approx_prior_exclusion)
        post_odds = prior_odds * 10
        post = post_odds / (1.0 + post_odds)
        observed_config1 = MsBayesConfig(sim_results.observed_index_to_config[1])
        observed_config2 = MsBayesConfig(sim_results.observed_index_to_config[1])
        cfg_to_num_ex = {observed_config1: bf_num_excluded,
                observed_config2: bf_num_excluded_glm}
        cfg_to_prob_exclusion = {observed_config1: prob_of_exclusion,
                observed_config2: prob_of_exclusion_glm}
        cfg_to_prob_of_bf_exclusion = {observed_config1: prob_of_bf_exclusion,
                observed_config2: prob_of_bf_exclusion_glm}
        ex_prob_plot = plotting.ProbabilityPowerPlotGrid(
                observed_config_to_estimates = cfg_to_prob_exclusion,
                variable = 'tau_exclusion',
                div_model_prior = 'psi',
                bayes_factor = 10,
                bayes_factor_prob = post,
                cfg_to_prob_of_bf_exclusion = cfg_to_prob_of_bf_exclusion,
                height = 3.7,
                margin_left = 0.03,
                margin_bottom = 0.06,
                margin_right = 1,
                margin_top = 0.96,
                padding_between_horizontal = 0.5,
                padding_between_vertical = 1.0,
                num_columns = 2)
        fig = ex_prob_plot.create_grid()
        fig.savefig(os.path.join(out_dir, 'prob_of_exclusion.pdf'))
        ex_plot = plotting.PowerPlotGrid(
                observed_config_to_estimates = cfg_to_num_ex,
                variable = 'tau_exclusion',
                num_columns = 2,
                height = 3.7,
                margin_left = 0.03,
                margin_bottom = 0.06,
                margin_right = 1,
                margin_top = 0.95,
                padding_between_horizontal = 0.5,
                padding_between_vertical = 1.0)
        fig = ex_plot.create_grid()
        fig.savefig(os.path.join(out_dir, 'num_tau_excluded.pdf'))


def main_cli():
    for sim_dir in ['m1-01-sim', 'm1-1-sim']:
        sim_info_path = os.path.join(project_util.RESULT_DIR, sim_dir,
                'pymsbayes-results', 'pymsbayes-info.txt')
        summarize_sim_results(sim_info_path)

if __name__ == '__main__':
    main_cli()

