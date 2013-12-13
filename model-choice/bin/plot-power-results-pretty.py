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

class TauExclusionResult(object):
    def __init__(self):
        self.num_excluded = []
        self.num_excluded_glm = []
        self.prob_of_exclusion = []
        self.prob_of_exclusion_glm = []
        self.prior_prob_of_exclusion = []
        self.bf_of_exclusion = []
        self.bf_of_exclusion_glm = []
        approx_prior_exclusion = 0.39184
        prior_odds = approx_prior_exclusion / (1.0 - approx_prior_exclusion)
        post_odds = prior_odds * 10
        self.bf_10_exclusion_prob = post_odds / (1.0 + post_odds)
        self.prob_of_bf_exclusion = None
        self.prob_of_bf_exclusion_glm = None

    def calc_prob_of_bf_exclusion(self):
        self.prob_of_bf_exclusion = (len([
                1 for x in self.bf_of_exclusion if x > 10.0]) /
                float(len(self.bf_of_exclusion)))
        self.prob_of_bf_exclusion_glm = (len([
                1 for x in self.bf_of_exclusion_glm if x > 10.0]) /
                float(len(self.bf_of_exclusion_glm)))

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
        tau = TauExclusionResult()
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

            tau.num_excluded.append(int(d['bf_num_excluded']))
            tau.num_excluded_glm.append(int(d['bf_num_excluded_glm']))
            tau.prob_of_exclusion.append(float(d['prob_of_exclusion']))
            tau.prob_of_exclusion_glm.append(float(d['prob_of_exclusion_glm']))
            tau.prior_prob_of_exclusion.append(float(d['prior_prob_of_exclusion']))
            tau.bf_of_exclusion.append(float(d['bf_of_exclusion']))
            tau.bf_of_exclusion_glm.append(float(d['bf_of_exclusion_glm']))
        tau.calc_prob_of_bf_exclusion()

        return psi, omega, tau

def parse_results(info_path):
    dmc_sim = DMCSimulationResults(info_path)
    psi_results = {}
    omega_results = {}
    observed_configs = {}
    tau_results = {}
    for k, v in dmc_sim.observed_index_to_config.iteritems():
        observed_configs[k] = MsBayesConfig(v)
    prior_index = '{0}-combined'.format(''.join(
            sorted([str(i) for i in dmc_sim.prior_index_to_config.iterkeys()])))
    for observed_index, cfg in observed_configs.iteritems():
        result_path = dmc_sim.get_result_summary_path(observed_index,
                prior_index)
        psi, omega, tau = PowerResult.parse_result_summary(result_path)
        psi_results[cfg] = psi
        omega_results[cfg] = omega
        tau_results[cfg] = tau
    return psi_results, omega_results, tau_results

def create_plots(info_path):
    output_dir = os.path.join(os.path.dirname(info_path), 'plots')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    prior_prob_omega_less_than = 0.0887
    psi_results, omega_results, tau_results = parse_results(info_path)
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

    cfg_to_num_excluded = {}
    cfg_to_num_excluded_glm = {}
    cfg_to_prob_of_exclusion = {}
    cfg_to_prob_of_exclusion_glm = {}
    cfg_to_prob_of_bf_ex = {}
    cfg_to_prob_of_bf_ex_glm = {}
    bf_10_exclusion_prob = None
    for cfg, tau in tau_results.iteritems():
        cfg_to_num_excluded[cfg] = tau.num_excluded
        cfg_to_num_excluded_glm[cfg] = tau.num_excluded_glm
        cfg_to_prob_of_exclusion[cfg] = tau.prob_of_exclusion
        cfg_to_prob_of_exclusion_glm[cfg] = tau.prob_of_exclusion_glm
        cfg_to_prob_of_bf_ex[cfg] = tau.prob_of_bf_exclusion
        cfg_to_prob_of_bf_ex_glm[cfg] = tau.prob_of_bf_exclusion_glm
        if not bf_10_exclusion_prob:
            bf_10_exclusion_prob = tau.bf_10_exclusion_prob

    psi_plot = PowerPlotGrid(observed_config_to_estimates = cfg_to_psi,
            variable = 'psi',
            num_columns = 2,
            x_title = r'Estimated number of divergence events, $\hat{\Psi}$',
            y_title = 'Density',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.85,
            padding_between_horizontal = 0.5)

    fig = psi_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 8.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-psi-mode-6.pdf'))

    psi_plot.width = 10.0
    fig = psi_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 12.0,
            x_tick_label_size = 8.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-psi-mode-4.pdf'))


    omega_prob_plot = ProbabilityPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_prob,
            variable = 'omega',
            div_model_prior = 'psi',
            bayes_factor = 10,
            bayes_factor_prob = prior_prob_omega_less_than,
            num_columns = 2,
            x_title = (r'Posterior probability of one divergence, '
                    r'$p(\Omega < 0.01 \, | \, B_{{\epsilon}}(S*))$'),
            y_title = 'Density',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.85,
            padding_between_horizontal = 0.5)
    fig = omega_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-omega-prob-6.pdf'))
    omega_prob_plot.width = 10.0
    fig = omega_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-omega-prob-4.pdf'))
    omega_prob_plot.label_offset = 6
    omega_prob_plot.width = 14.0
    fig = omega_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-omega-prob-6-panel.pdf'))
    omega_prob_plot.label_offset = 4
    omega_prob_plot.width = 10.0
    fig = omega_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-omega-prob-4-panel.pdf'))
    
    omega_accuracy_plot = AccuracyPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_true_ests,
            num_columns = 2,
            x_title = r'True variance of divergence times, $\Omega$',
            y_title = r'$\hat{\Omega}$',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.83,
            padding_between_horizontal = 0.5)
    fig = omega_accuracy_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-median-6.pdf'))
    omega_accuracy_plot.width = 10.0
    fig = omega_accuracy_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-median-4.pdf'))

    omega_accuracy_plot_glm = AccuracyPowerPlotGrid(
            observed_config_to_estimates = cfg_to_omega_true_ests_glm,
            num_columns = 2,
            x_title = r'True variance of divergence times, $\Omega$',
            y_title = r'$\hat{\Omega}$',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.83,
            padding_between_horizontal = 0.5)
    fig = omega_accuracy_plot_glm.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-mode-glm-6.pdf'))
    omega_accuracy_plot_glm.width = 10.0
    fig = omega_accuracy_plot_glm.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-mode-glm-4.pdf'))
    omega_accuracy_plot_glm.label_offset = 6
    omega_accuracy_plot_glm.width = 14.0
    fig = omega_accuracy_plot_glm.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-mode-glm-6-panel.pdf'))
    omega_accuracy_plot_glm.label_offset = 4
    omega_accuracy_plot_glm.width = 10.0
    fig = omega_accuracy_plot_glm.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = False,
            share_y = False)
    fig.savefig(os.path.join(output_dir, 'power-accuracy-omega-mode-glm-4-panel.pdf'))

    ex_prob_plot = ProbabilityPowerPlotGrid(
            observed_config_to_estimates = cfg_to_prob_of_exclusion,
            variable = 'tau_exclusion',
            div_model_prior = 'psi',
            bayes_factor = 10,
            bayes_factor_prob = bf_10_exclusion_prob,
            cfg_to_prob_of_bf_exclusion = cfg_to_prob_of_bf_ex,
            num_columns = 2,
            x_title = (r'Posterior probability of excluding true parameters, $p(\mathbf{\tau} \, \notin \, '
                        r'M \, | \, B_{\epsilon}(S*))$'),
            y_title = 'Density',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.85,
            padding_between_horizontal = 0.5)
    fig = ex_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-prob-exclusion-6.pdf'))
    ex_prob_plot.width = 10.0
    fig = ex_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-prob-exclusion-4.pdf'))
    ex_prob_plot.label_offset = 6
    ex_prob_plot.width = 14.0
    fig = ex_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-prob-exclusion-6-panel.pdf'))
    ex_prob_plot.label_offset = 4
    ex_prob_plot.width = 10.0
    fig = ex_prob_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            add_column_labels = False,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 10.0,
            x_tick_label_size = 10.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-prob-exclusion-4-panel.pdf'))


    ex_plot = PowerPlotGrid(
            observed_config_to_estimates = cfg_to_num_excluded,
            variable = 'tau_exclusion',
            num_columns = 2,
            x_title = r'Number of true $\tau$ excluded',
            y_title = 'Density',
            width = 14.0,
            height = 2.8,
            auto_height = False,
            auto_adjust_margins = False,
            margin_left = 0.025,
            margin_bottom = 0.1,
            margin_right = 1,
            margin_top = 0.85,
            padding_between_horizontal = 0.5)

    fig = ex_plot.create_column_grid(
            subplot_indices_to_exclude = [],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            x_tick_label_size = 8.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-num-excluded-6.pdf'))
    ex_plot.width = 10.0
    fig = ex_plot.create_column_grid(
            subplot_indices_to_exclude = [1,3],
            x_title_size = 14.0,
            y_title_size = 14.0,
            column_label_size = 16.0,
            column_label_offset = 0.14,
            right_text_size = 12.0,
            x_tick_label_size = 8.0,
            share_x = True,
            share_y = True)
    fig.savefig(os.path.join(output_dir, 'power-num-excluded-4.pdf'))

def main_cli():
    if len(sys.argv) != 2:
        sys.stderr.write('This script requires one argument: The path to the '
                'power analysis `pymsbayes-info.txt` file')
        sys.exit(1)
    info_path = sys.argv[1]
    create_plots(info_path)

if __name__ == '__main__':
    main_cli()

