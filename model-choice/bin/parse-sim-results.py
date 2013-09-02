#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import (DMCSimulationResults,
        parse_posterior_summary_file, dict_line_iter)
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)
SIM_INFO_PATH = os.path.join(project_util.RESULT_DIR, 'm1-01-sim',
        'pymsbayes-results', 'pymsbayes-info.txt')
OUT_PATH = os.path.join(os.path.dirname(SIM_INFO_PATH), 'results-summary.txt')
NUM_SIMS = 1000

def get_sublist_greater_than(values, threshold):
    return [v for v in values if v > threshold]

def main_cli():
    model_to_tau_max = {'m1-01': 0.01,
            'm2': 1.0,
            'm3': 5.0,
            'm4': 10.0,
            'm5': 20.0}
    sim_results = DMCSimulationResults(SIM_INFO_PATH)
    index_to_model = {}
    for k, v in sim_results.prior_config_to_index.iteritems():
        index_to_model[v] = k
    excluded = []
    ex_tally = 0
    excluded_glm = []
    ex_tally_glm = 0
    d = {'model_mode': [], 'model_mode_glm': [], 'tau_max': [],
            'tau_max_glm': [], 'num_excluded': [], 'num_excluded_glm': []}
    for i in range(1, 23):
        d['tau_' + str(i)] = []
    for i, (true_params, paths) in enumerate(sim_results.result_path_iter(1,
            '12345-combined')):
        div_times = sorted([float(true_params['PRI.t.' + str(i)]) for i in range(
                1, 23)])
        for i, t in enumerate(div_times):
            d['tau_' + str(i + 1)].append(t)
        results = sim_results.get_results_from_params_and_result_paths(
                true_params, paths)
        model_index = results['model']['mode']
        model_index_glm = int(round(results['model']['mode_glm']))
        tau_max = model_to_tau_max[index_to_model[model_index]] 
        tau_max_glm = model_to_tau_max[index_to_model[model_index_glm]]
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
    assert len(excluded) == NUM_SIMS
    assert len(excluded_glm) == NUM_SIMS
    for k, v in d.iteritems():
        assert len(v) == NUM_SIMS, '{0!r} has {1} values'.format(k, len(v))
    assert len([0 for x in excluded if len(x) > 0]) == ex_tally
    assert len([0 for x in excluded_glm if len(x) > 0]) == ex_tally_glm
    sys.stdout.write('Proportion of simulations excluding truth: {0}'.format(
            ex_tally / float(NUM_SIMS)))
    sys.stdout.write('Proportion of simulations excluding truth with GLM-'
            'adjustment: {0}'.format(ex_tally_glm / float(NUM_SIMS)))
    with open(OUT_PATH, 'w') as out:
        for line in dict_line_iter(d):
            out.write(line)

if __name__ == '__main__':
    main_cli()
