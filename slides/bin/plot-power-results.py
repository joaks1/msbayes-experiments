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

def parse_results(dmc_sim,
        observed_prefixes_to_include = None,
        observed_suffixes_to_include = None,
        prior_suffixes_to_include = None):
    psi_results = {}
    omega_results = {}
    observed_index_to_name = {}
    observed_configs = {}
    for k, v in dmc_sim.observed_index_to_config.iteritems():
        if observed_prefixes_to_include:
            include = False
            for s in observed_prefixes_to_include:
                if os.path.basename(v).startswith(s):
                    include = True
                    break
            if not include:
                continue
        if observed_suffixes_to_include:
            include = False
            for s in observed_suffixes_to_include:
                if os.path.splitext(v)[0].endswith(s):
                    include = True
                    break
            if not include:
                continue
        if os.path.basename(v).startswith('exp-'):
            observed_index_to_name[k] = 'exp'
        elif os.path.basename(v).startswith('old-'):
            observed_index_to_name[k] = 'old'
        elif os.path.basename(v).startswith('observed'):
            observed_index_to_name[k] = 'uniform'
        else:
            raise Exception('unrecognized observed config {0!r}'.format(v))
        observed_configs[k] = MsBayesConfig(v)

    prior_index_to_name = {}
    for k, v in dmc_sim.prior_index_to_config.iteritems():
        n = os.path.splitext(os.path.basename(v))[0]
        n = n.split('-')[1:]
        n = '-'.join(n)
        if prior_suffixes_to_include and (not n in prior_suffixes_to_include):
            continue
        prior_index_to_name[k] = n

    for observed_index, cfg in observed_configs.iteritems():
        observed_name = observed_index_to_name[observed_index]
        if not psi_results.has_key(observed_name):
            psi_results[observed_name] = {}
        if not omega_results.has_key(observed_name):
            omega_results[observed_name] = {}
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

def create_plots(info_path,
        observed_prefixes_to_include = None,
        observed_suffixes_to_include = None,
        prior_suffixes_to_include = None):
    dmc_sim = DMCSimulationResults(info_path)
    prior_configs = {}
    for k, v in dmc_sim.prior_index_to_config.iteritems():
        prior_configs[k] = MsBayesConfig(v)
    # output_dir = os.path.join(os.path.dirname(info_path), 'plots')
    output_dir = project_util.IMAGE_DIR
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    prior_prob_omega_less_than = {
            1: 0.0025575,
            2: 0.049283,
            3: 0.002171,
            4: 0.049191}
    psi_res, omega_res, prior_index_to_name = parse_results(dmc_sim,
            observed_prefixes_to_include = observed_prefixes_to_include,
            observed_suffixes_to_include = observed_suffixes_to_include,
            prior_suffixes_to_include = prior_suffixes_to_include)
    for observed_name in psi_res.iterkeys():
        for prior_index in psi_res[observed_name].iterkeys():
            prior_name = prior_index_to_name[prior_index]
            div_model_prior = prior_name
            if prior_name in ['old', 'u-shaped']:
                div_model_prior = 'psi'
            dpp_concentration_mean = None
            if div_model_prior == 'dpp':
                dpp_concentration_mean = prior_configs[
                        prior_index].dpp_concentration.mean
            prior_prob_omega = prior_prob_omega_less_than[prior_index]
            psi_results = psi_res[observed_name][prior_index]
            omega_results = omega_res[observed_name][prior_index]
            prefix = '_'.join([observed_name, prior_name])
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

            num_columns = len(observed_suffixes_to_include)
            width = 15
            height = 3.5
            column_label_offset = 0.14
            margin_top = 0.83
            margin_bottom = 0.1
            margin_left = 0.025
            margin_right = 0.95
            column_label_size = 26.0
            title_size = 22.0
            y_title_size = 20.0
            right_text_size = 14.0
            row_labels = []
            if prior_name == 'old':
                row_labels.append(r'$M_{msBayes}$')
            elif prior_name == 'u-shaped':
                row_labels.append(r'$M_{Ushaped}$')
            elif prior_name == 'uniform':
                row_labels.append(r'$M_{Uniform}$')
            elif prior_name == 'dpp':
                row_labels.append(r'$M_{DPP}$')
            else:
                row_labels.append('')
            row_label_size = 32.0
            row_label_offset = 0.08


            psi_plot = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi,
                    variable = 'psi',
                    variable_symbol = r'|\mathbf{\tau}|',
                    num_columns = num_columns,
                    width = width,
                    height = height,
                    x_title = r'Estimated number of divergence events (mode)',
                    y_title_size = y_title_size,
                    include_right_text = False,
                    text_size = right_text_size,
                    xtick_label_size = 14.0)
            pg = psi_plot.create_grid()
            pg.label_schema = None
            column_labels = []
            for cfg, sp in psi_plot.cfg_to_subplot.iteritems():
                column_labels.append((cfg.tau.maximum, tau_prior_in_generations(cfg)))
                sp.set_left_text('')
            pg.column_labels = [t for (c, t) in sorted(column_labels, key = lambda x : x[0])]
            pg.margin_bottom = margin_bottom
            pg.margin_top = margin_top
            pg.margin_left = margin_left
            pg.margin_right = margin_right
            pg.padding_between_horizontal = 2.0
            pg.column_label_offset = column_label_offset
            pg.column_label_size = column_label_size
            pg.title_size = title_size
            pg.row_labels = row_labels
            pg.row_label_size = row_label_size
            pg.row_label_offset = row_label_offset
            pg.reset_figure()
            pg.set_shared_x_limits()
            pg.set_shared_y_limits()
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_mode.pdf'))
            pg.column_labels = ['' for x in column_labels]
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_mode_headless.pdf'))

            # psi_plot_glm = PowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_psi_glm,
            #         variable = 'psi',
            #         variable_symbol = r'|\mathbf{\tau}|',
            #         num_columns = 2,
            #         margin_top = 0.975)
            # fig = psi_plot_glm.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_psi_mode_glm.pdf'))

            psi_prob_plot = ProbabilityPowerPlotGrid(
                    observed_config_to_estimates = cfg_to_psi_prob,
                    variable = 'psi',
                    variable_symbol = r'|\mathbf{\tau}|',
                    div_model_prior = div_model_prior,
                    dpp_concentration_mean = dpp_concentration_mean,
                    bayes_factor = 10,
                    draw_bayes_factor_line = False,
                    x_title = r'Posterior probability of one divergence',
                    y_title_size = y_title_size,
                    width = width,
                    height = height,
                    num_columns = num_columns,
                    text_size = right_text_size,
                    xtick_label_size = 14.0,
                    pretty_xtick_labels = True)
            pg = psi_prob_plot.create_grid()
            pg.label_schema = None
            column_labels = []
            for cfg, sp in psi_prob_plot.cfg_to_subplot.iteritems():
                column_labels.append((cfg.tau.maximum, tau_prior_in_generations(cfg)))
                sp.set_left_text('')
                sp.set_right_text('')
            pg.column_labels = [t for (c, t) in sorted(column_labels, key = lambda x : x[0])]
            pg.margin_bottom = margin_bottom
            pg.margin_top = margin_top
            pg.margin_left = margin_left
            pg.margin_right = margin_right
            pg.column_label_offset = column_label_offset
            pg.column_label_size = column_label_size
            pg.padding_between_horizontal = 1.0
            pg.title_size = title_size
            pg.row_labels = row_labels
            pg.row_label_size = row_label_size
            pg.row_label_offset = row_label_offset
            pg.reset_figure()
            pg.set_shared_x_limits()
            pg.set_shared_y_limits()
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_prob.pdf'))
            pg.column_labels = ['' for x in column_labels]
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_psi_prob_headless.pdf'))

            # psi_prob_plot_glm = ProbabilityPowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_psi_prob_glm,
            #         variable = 'psi',
            #         variable_symbol = r'|\mathbf{\tau}|',
            #         div_model_prior = div_model_prior,
            #         dpp_concentration_mean = dpp_concentration_mean,
            #         bayes_factor = 10,
            #         num_columns = 2)
            # fig = psi_prob_plot_glm.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_psi_prob_glm.pdf'))

            omega_plot = PowerPlotGrid(
                    observed_config_to_estimates = cfg_to_omega,
                    variable = 'omega',
                    variable_symbol = r'D_T',
                    num_columns = num_columns,
                    width = width,
                    height = height,
                    x_title = r'Estimated variance in divergence times (median)',
                    y_title_size = y_title_size,
                    text_size = right_text_size)
            pg = omega_plot.create_grid()
            pg.label_schema = None
            column_labels = []
            for cfg, sp in omega_plot.cfg_to_subplot.iteritems():
                column_labels.append((cfg.tau.maximum, tau_prior_in_generations(cfg)))
                sp.set_left_text('')
            pg.column_labels = [t for (c, t) in sorted(column_labels, key = lambda x : x[0])]
            pg.margin_bottom = margin_bottom
            pg.margin_top = margin_top
            pg.margin_left = margin_left
            pg.margin_right = margin_right
            pg.column_label_offset = column_label_offset
            pg.column_label_size = column_label_size
            pg.title_size = title_size
            pg.row_labels = row_labels
            pg.row_label_size = row_label_size
            pg.row_label_offset = row_label_offset
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_median.pdf'))
            pg.column_labels = ['' for x in column_labels]
            pg.reset_figure()
            pg.savefig(os.path.join(output_dir,
                    prefix + '_power_omega_median_headless.pdf'))

            # omega_plot_glm = PowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_omega_glm,
            #         variable = 'omega',
            #         variable_symbol = r'D_T',
            #         num_columns = 2)
            # fig = omega_plot_glm.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_omega_mode_glm.pdf'))

            # omega_prob_plot = ProbabilityPowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_omega_prob,
            #         variable = 'omega',
            #         variable_symbol = r'D_T',
            #         div_model_prior = div_model_prior,
            #         dpp_concentration_mean = dpp_concentration_mean,
            #         bayes_factor = 10,
            #         bayes_factor_prob = prior_prob_omega,
            #         num_columns = 2,
            #         text_size = 10.0)
            # fig = omega_prob_plot.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_omega_prob.pdf'))

            # omega_prob_plot_glm = ProbabilityPowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_omega_prob_glm,
            #         variable = 'omega',
            #         variable_symbol = r'D_T',
            #         div_model_prior = div_model_prior,
            #         dpp_concentration_mean = dpp_concentration_mean,
            #         bayes_factor = 10,
            #         bayes_factor_prob = prior_prob_omega,
            #         num_columns = 2,
            #         text_size = 10.0)
            # fig = omega_prob_plot_glm.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_omega_prob_glm.pdf'))
            
            # omega_accuracy_plot = AccuracyPowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_omega_true_ests,
            #         variable_symbol = r'D_T',
            #         num_columns = 2,
            #         padding_between_vertical = 2.0,
            #         margin_left = 0.04,
            #         margin_bottom = 0.03)
            # fig = omega_accuracy_plot.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_accuracy_omega_median.pdf'))

            # omega_accuracy_plot_glm = AccuracyPowerPlotGrid(
            #         observed_config_to_estimates = cfg_to_omega_true_ests_glm,
            #         variable_symbol = r'D_T',
            #         num_columns = 2,
            #         padding_between_vertical = 2.0,
            #         margin_left = 0.04,
            #         margin_bottom = 0.03)
            # fig = omega_accuracy_plot_glm.create_grid()
            # fig.savefig(os.path.join(output_dir,
            #         prefix + '_power_accuracy_omega_mode_glm.pdf'))

def tau_prior_in_generations(cfg, mu = 1e-8):
    upper_tau = (cfg.tau.maximum * (cfg.theta.mean / mu)) / 1000000.0
    return r'$\tau \sim U(0, \, {0:.1f} \, \mathsf{{MGA}})$'.format(upper_tau)

def main_cli():
    if len(sys.argv) != 2:
        sys.stderr.write('This script requires one argument: The path to the '
                'power analysis `pymsbayes-info.txt` file')
        sys.exit(1)
    info_path = sys.argv[1]
    observed_prefixes_to_include = ['old']
    observed_suffixes_to_include = ['0.2', '0.6', '1.0', '2.0']
    prior_suffixes_to_include = ['dpp', 'old', 'u-shaped']
    create_plots(info_path,
            observed_prefixes_to_include = observed_prefixes_to_include,
            observed_suffixes_to_include = observed_suffixes_to_include,
            prior_suffixes_to_include = prior_suffixes_to_include)

if __name__ == '__main__':
    main_cli()

