#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults, spreadsheet_iter
from pymsbayes.config import MsBayesConfig
from pymsbayes.plotting import (PowerPlotGrid, ProbabilityPowerPlotGrid,
        AccuracyPowerPlotGrid)
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

class PowerResult(object):
    def __init__(self):
        self.true = []
        self.mode = []
        self.mode_glm = []
        self.median = []
        self.prob = []
        self.prob_glm = []

    @classmethod
    def parse_result_summary(cls, result_summary_path):
        psi = cls()
        omega = cls()
        for d in spreadsheet_iter([result_summary_path]):
            psi.true.append(int(d['psi_true']))
            psi.mode.append(int(d['psi_mode']))
            psi.mode_glm.append(int(round(float(d['psi_mode_glm']))))
            psi.prob.append(float(d['psi_1_prob']))
            psi.prob_glm.append(float(d['psi_1_prob_glm']))
            omega.true.append(float(d['omega_true']))
            omega.mode.append(float(d['omega_mode']))
            omega.median.append(float(d['omega_median']))
            omega.mode_glm.append(float(d['omega_mode_glm']))
            omega.prob.append(float(d['omega_prob_less']))
            omega.prob_glm.append(float(d['omega_prob_less_glm']))
        return psi, omega

def parse_results(info_path):
    dmc_sim = DMCSimulationResults(info_path)
    psi_results = {}
    omega_results = {}
    observed_configs = {}
    for k, v in dmc_sim.observed_index_to_config.iteritems():
        observed_configs[k] = MsBayesConfig(v)
    prior_index = '{0}-combined'.format(''.join(
            sorted([str(i) for i in dmc_sim.prior_index_to_config.iterkeys()])))
    for observed_index, cfg in observed_configs.iteritems():
        result_path = dmc_sim.get_result_summary_path(observed_index,
                prior_index)
        psi, omega = PowerResult.parse_result_summary(result_path)
        psi_results[cfg] = psi
        omega_results[cfg] = omega
    return psi_results, omega_results

def create_plots(info_path):
    output_dir = os.path.join(os.path.dirname(info_path), 'plots')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    prior_prob_omega_less_than = 0.0887
    psi_results, omega_results = parse_results(info_path)
    cfg_to_psi = {}
    cfg_to_psi_prob = {}
    for cfg, psi in psi_results.iteritems():
        cfg_to_psi[cfg] = psi.mode
        cfg_to_psi_prob[cfg] = psi.prob
    cfg_to_omega = {}
    cfg_to_omega_prob = {}
    cfg_to_omega_true_ests = {}
    cfg_to_omega_true_ests_glm = {}
    for cfg, omega in omega_results.iteritems():
        cfg_to_omega[cfg] = omega.median
        cfg_to_omega_prob[cfg] = omega.prob
        cfg_to_omega_true_ests[cfg] = {'x': omega.true, 'y': omega.median}
        cfg_to_omega_true_ests_glm[cfg] = {'x': omega.true, 'y': omega.mode_glm}

    psi_plot = PowerPlotGrid(observed_config_to_estimates = cfg_to_psi,
            variable = 'psi',
            num_columns = 2)
    fig = psi_plot.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_psi_mode.pdf'))

    psi_prob_plot = ProbabilityPowerPlotGrid(
            observed_config_to_estimates = cfg_to_psi_prob,
            variable = 'psi',
            div_model_prior = 'psi',
            bayes_factor = 10,
            num_columns = 2)
    fig = psi_prob_plot.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_psi_prob.pdf'))

    omega_plot = PowerPlotGrid(observed_config_to_estimates = cfg_to_omega,
            variable = 'omega',
            num_columns = 2)
    fig = omega_plot.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_omega_median.pdf'))

    omega_prob_plot = ProbabilityPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_prob,
            variable = 'omega',
            div_model_prior = 'psi',
            bayes_factor = 10,
            bayes_factor_prob = prior_prob_omega_less_than,
            num_columns = 2)
    fig = omega_prob_plot.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_omega_prob.pdf'))
    
    omega_accuracy_plot = AccuracyPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_true_ests,
            num_columns = 2)
    fig = omega_accuracy_plot.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_accuracy_omega_median.pdf'))

    omega_accuracy_plot_glm = AccuracyPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_true_ests_glm,
            num_columns = 2)
    fig = omega_accuracy_plot_glm.create_grid()
    fig.savefig(os.path.join(output_dir, 'power_accuracy_omega_mode_glm.pdf'))

def main_cli():
    if len(sys.argv) != 2:
        sys.stderr.write('This script requires one argument: The path to the '
                'power analysis `pymsbayes-info.txt` file')
        sys.exit(1)
    info_path = sys.argv[1]
    create_plots(info_path)

if __name__ == '__main__':
    main_cli()

