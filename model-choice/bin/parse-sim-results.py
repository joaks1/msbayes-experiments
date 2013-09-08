#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import (DMCSimulationResults,
        parse_posterior_summary_file, dict_line_iter)
from pymsbayes.config import MsBayesConfig
from pymsbayes.fileio import process_file_arg, expand_path
from pymsbayes.utils.stats import mode_list
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def get_sublist_greater_than(values, threshold):
    return [v for v in values if v > threshold]

def parse_sim_results(info_path, num_sims, num_taxon_pairs):
    info_path = expand_path(info_path)
    sim_results = DMCSimulationResults(info_path)
    out_dir = os.path.dirname(info_path)
    summary_path = os.path.join(out_dir, 'results-summary.txt')
    results_path = os.path.join(out_dir, 'results.txt.gz')
    model_configs = {}
    for k, v in sim_results.prior_index_to_config.iteritems():
        model_configs[k] = MsBayesConfig(v)
    excluded = []
    ex_tally = 0
    excluded_glm = []
    ex_tally_glm = 0
    d = {'model_mode': [], 'model_mode_glm': [], 'tau_max': [],
            'tau_max_glm': [], 'num_excluded': [], 'num_excluded_glm': []}
    for i in range(1, num_taxon_pairs + 1):
        d['tau_' + str(i)] = []
    for i, (true_params, paths) in enumerate(sim_results.result_path_iter(1,
            '12345-combined')):
        div_times = sorted([float(true_params['PRI.t.' + str(i)]) for i in range(
                1, num_taxon_pairs + 1)])
        for i, t in enumerate(div_times):
            d['tau_' + str(i + 1)].append(t)
        results = sim_results.get_results_from_params_and_result_paths(
                true_params, paths)
        model_index = results['model']['mode']
        model_index_glm = int(round(results['model']['mode_glm']))
        tau_max = model_configs[model_index].tau.maximum 
        tau_max_glm = model_configs[model_index_glm].tau.maximum
        ex = get_sublist_greater_than(div_times, tau_max)
        if len(ex) > 0:
            ex_tally += 1
        ex_glm = get_sublist_greater_than(div_times, tau_max_glm)
        if len(ex_glm) > 0:
            ex_tally_glm += 1
        excluded.append(ex)
        excluded_glm.append(ex_glm)
        d['model_mode'].append(model_index)
        d['model_mode_glm'].append(model_index_glm)
        d['tau_max'].append(tau_max)
        d['tau_max_glm'].append(tau_max_glm)
        d['num_excluded'].append(len(ex))
        d['num_excluded_glm'].append(len(ex_glm))
    assert len(excluded) == num_sims
    assert len(excluded_glm) == num_sims
    for k, v in d.iteritems():
        assert len(v) == num_sims, '{0!r} has {1} values'.format(k, len(v))
    assert len([0 for x in excluded if len(x) > 0]) == ex_tally
    assert len([0 for x in excluded_glm if len(x) > 0]) == ex_tally_glm
    with open(summary_path, 'w') as summary_stream:
        summary_stream.write('Proportion of simulations excluding truth: {0}\n'.format(
                ex_tally / float(num_sims)))
        summary_stream.write('Proportion of simulations excluding truth with GLM-'
                'adjustment: {0}\n'.format(ex_tally_glm / float(num_sims)))
        summary_stream.write('Average number of tau parameters excluded: {0}\n'.format(
                sum(d['num_excluded']) / float(num_sims)))
        summary_stream.write('Average number of tau parameters excluded with GLM: '
                '{0}\n'.format(sum(d['num_excluded_glm']) / float(num_sims)))
        summary_stream.write('Mode number of tau parameters excluded: {0}\n'.format(
                mode_list(d['num_excluded'])))
        summary_stream.write('Mode number of tau parameters excluded with GLM: '
                '{0}\n'.format(mode_list(d['num_excluded_glm'])))
        summary_stream.write('Max number of tau parameters excluded: {0}\n'.format(
                max(d['num_excluded'])))
        summary_stream.write('Max number of tau parameters excluded with GLM: '
                '{0}\n'.format(max(d['num_excluded_glm'])))
    results_stream, close = process_file_arg(results_path, 'w', compresslevel=9)
    for line in dict_line_iter(d):
        results_stream.write(line)
    results_stream.close()

def main_cli():
    num_taxon_pairs = 22
    num_sims = 1000
    for sim_dir in ['m1-01-sim', 'm1-1-sim']:
        sim_info_path = os.path.join(project_util.RESULT_DIR, sim_dir,
                'pymsbayes-results', 'pymsbayes-info.txt')
        parse_sim_results(sim_info_path, num_sims, num_taxon_pairs)

if __name__ == '__main__':
    main_cli()

