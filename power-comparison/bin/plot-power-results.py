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
    observed_index_to_name = {}
    observed_configs = {}
    for k, v in dmc_sim.observed_index_to_config.iteritems():
        if os.path.basename(v).startwith('exp-'):
            observed_index_to_name[k] = 'exp'
        elif os.path.basename(v).startwith('old-'):
            observed_index_to_name[k] = 'old'
        elif os.path.basename(v).startwith('observed'):
            observed_index_to_name[k] = 'uniform'
        else:
            raise Exception('unrecognized observed config {0!r}'.format(v))
        observed_configs[k] = MsBayesConfig(v)

    prior_index_to_name = {}
    for k, v in dmc_sim.prior_index_to_config.iteritems():
        n = os.path.splitext(os.path.basename(v))[0]
        n = n.split('-')[1:]
        n = '-'.join(n)
        prior_index_to_name[k] = n

    for observed_index, cfg in observed_configs.iteritems():
        observed_name = observed_index_to_name[observed_index]
        if not psi_results.has_key(observed_name):
            psi_reults[observed_name] = {}
        if not omega_results.has_key(observed_name):
            omega_reults[observed_name] = {}
        for prior_index in prior_index_to_name.iterkeys():
            if not psi_results[observed_name].has_key(prior_index):
                psi_results[observed_name][prior_index] = {}
            if not omega_results[observed_name].has_key(prior_index):
                omega_results[observed_name][prior_index] = {}
            result_path = dmc_sim.get_result_summary_path(observed_index,
                    prior_index)
            psi, omega = PowerResult.parse_result_summary(result_path)
            psi_results[observed_name][prior_index][cfg] = psi
            omega_results[observed_name][prior_index][cfg] = omega
    return psi_results, omega_results, prior_index_to_name

def create_plots(info_path):
    output_dir = os.path.join(os.path.dirname(info_path), 'plots')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    prior_prob_omega_less_than = {
            1: 0.0025575,
            2: 0.049283,
            3: 0.002171,
            4: 0.049191}
    psi_res, omega_res, prior_index_to_name = parse_results(info_path)
    for observed_name in psi_res.iterkeys():
        for prior_index in psi_res[observed_name].iterkeys():
            prior_name = prior_index_to_name[prior_index]
            prior_prob_omega = prior_prob_omega_less_than[prior_index]
            psi_results = psi_res[observed_name][prior_index]
            omega_results = omega_res[observed_name][prior_index]
            prefix = '_'.join(observed_name, prior_name)
            cfg_to_psi = {}
            cfg_to_psi_prob = {}
            cfg_to_psi_glm = {}
            cfg_to_psi_prob_glm = {}
            for cfg, psi in psi_results.iteritems():
                cfg_to_psi[cfg] = psi.mode
                cfg_to_psi_prob[cfg] = psi.prob
                cfg_to_psi_glm[cfg] = psi.mode_glm
                cfg_to_psi_prob_glm[cfg] = psi.prob_glm
            cfg_to_omega = {}
            cfg_to_omega_prob = {}
            cfg_to_omega_glm = {}
            cfg_to_omega_prob_glm = {}
            cfg_to_omega_true_ests = {}
            cfg_to_omega_true_ests_glm = {}
            for cfg, omega in omega_results.iteritems():
                cfg_to_omega[cfg] = omega.median
                cfg_to_omega_prob[cfg] = omega.prob
                cfg_to_omega_glm[cfg] = omega.mode_glm
                cfg_to_omega_prob_glm[cfg] = omega.prob_glm
                cfg_to_omega_true_ests[cfg] = {'x': omega.true, 'y': omega.median}
                cfg_to_omega_true_ests_glm[cfg] = {'x': omega.true, 'y': omega.mode_glm}

            psi_plot = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi,
                    variable = 'psi',
                    num_columns = 2)
            fig = psi_plot.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_mode.pdf'))

            psi_plot_glm = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi_glm,
                    variable = 'psi',
                    num_columns = 2)
            fig = psi_plot_glm.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_mode_glm.pdf'))

            psi_prob_plot = ProbabilityPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi_prob,
                    variable = 'psi',
                    div_model_prior = 'psi',
                    bayes_factor = 10,
                    num_columns = 2)
            fig = psi_prob_plot.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_prob.pdf'))

            psi_prob_plot_glm = ProbabilityPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi_prob_glm,
                    variable = 'psi',
                    div_model_prior = 'psi',
                    bayes_factor = 10,
                    num_columns = 2)
            fig = psi_prob_plot_glm.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_prob_glm.pdf'))

            omega_plot = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega,
                    variable = 'omega',
                    num_columns = 2)
            fig = omega_plot.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_median.pdf'))

            omega_plot_glm = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega_glm,
                    variable = 'omega',
                    num_columns = 2)
            fig = omega_plot_glm.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_mode_glm.pdf'))

            omega_prob_plot = ProbabilityPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega_prob,
                    variable = 'omega',
                    div_model_prior = 'psi',
                    bayes_factor = 10,
                    bayes_factor_prob = prior_prob_omega,
                    num_columns = 2)
            fig = omega_prob_plot.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_prob.pdf'))

            omega_prob_plot_glm = ProbabilityPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega_prob_glm,
                    variable = 'omega',
                    div_model_prior = 'psi',
                    bayes_factor = 10,
                    bayes_factor_prob = prior_prob_omega,
                    num_columns = 2)
            fig = omega_prob_plot_glm.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_prob_glm.pdf'))
            
            omega_accuracy_plot = AccuracyPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega_true_ests,
                    num_columns = 2)
            fig = omega_accuracy_plot.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_accuracy_omega_median.pdf'))

            omega_accuracy_plot_glm = AccuracyPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega_true_ests_glm,
                    num_columns = 2)
            fig = omega_accuracy_plot_glm.create_grid()
            fig.savefig(os.path.join(output_dir,
                    prefix + '_power_accuracy_omega_mode_glm.pdf'))

def main_cli():
    if len(sys.argv) != 2:
        sys.stderr.write('This script requires one argument: The path to the '
                'power analysis `pymsbayes-info.txt` file')
        sys.exit(1)
    info_path = sys.argv[1]
    create_plots(info_path)

if __name__ == '__main__':
    main_cli()

