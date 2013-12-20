#! /usr/bin/env python

import os
import sys

import matplotlib

from pymsbayes import teams
from pymsbayes.utils.parsing import DMCSimulationResults, spreadsheet_iter
from pymsbayes.config import MsBayesConfig
from pymsbayes.plotting import (Ticks, HistData, ScatterPlot, PlotGrid)
from pymsbayes.utils import stats, parsing, GLOBAL_RNG
from pymsbayes.utils.stats import Partition
from pymsbayes.utils.probability import GammaDistribution
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def get_divergence_model_probs(num_divergence_probs):
    ips = stats.IntegerPartition.number_of_int_partitions_by_k(
            num_elements = len(num_divergence_probs))
    div_model_probs = {}
    for k, p in num_divergence_probs.iteritems():
        div_model_probs[k] = p / float(ips[k-1])
    return div_model_probs

def get_dpp_prior_probs(config_path, num_samples = 100000):
    prob_team = teams.ModelProbabilityEstimatorTeam(
            config_paths = [config_path],
            num_samples = num_samples,
            num_processors = 8)
    prob_team.start()
    num_div_probs = prob_team.psi_probs[config_path]
    div_model_probs = get_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs

def get_dpp_prior_values(config_path, num_samples = 100000):
    num_div_probs, div_model_probs = get_dpp_prior_probs(
            config_path,
            num_samples)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples))

def get_uniform_prior_probs(npairs):
    ips = stats.IntegerPartition.number_of_int_partitions_by_k(
            num_elements = npairs)
    n = sum(ips)
    num_div_probs = {}
    for i in range(1, npairs + 1):
        num_div_probs[i] = ips[i-1] / float(n)
    div_model_probs = get_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs

def get_uniform_prior_values(npairs, num_samples = 10000):
    num_div_probs, div_model_probs = get_uniform_prior_probs(npairs)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples))

def get_psi_uniform_prior_probs(npairs):
    num_div_probs = {}
    for i in range(1, npairs + 1):
        num_div_probs[i] = 1.0 / npairs
    div_model_probs = get_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs

def get_psi_uniform_prior_values(npairs, num_samples = 10000):
    num_div_probs, div_model_probs = get_psi_uniform_prior_probs(npairs)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples))

def get_probs_from_psi_path(psi_path):
    probs = {}
    for d in spreadsheet_iter([psi_path]):
        probs[int(d['num_of_div_events'])] = float(d['estimated_prob'])
    return probs

def get_omega_from_summary_path(summary_path):
    results = parsing.parse_posterior_summary_file(summary_path)
    omega = float(results['PRI.omega']['median'])
    hpd = [float(results['PRI.omega']['HPD_95_interval'][0]),
            float(results['PRI.omega']['HPD_95_interval'][1])]
    if hpd[0] < 0.0:
        hpd[0] = 0.0
    return omega, (hpd[0], hpd[1])

def get_values_from_probs(probs, num_samples = 10000):
    v = []
    for k, p in probs.iteritems():
        n = int(round(num_samples * p))
        v.extend([k] * n)
    return v

def get_values_psi_path(psi_path, num_samples = 10000):
    probs = get_probs_from_psi_path(psi_path)
    return get_values_from_probs(probs, num_samples)

def get_histograms(config_path,
        info_path,
        num_samples = 10000):
    cfg = MsBayesConfig(config_path)
    dmc = DMCSimulationResults(info_path)
    npairs = dmc.num_taxon_pairs

    psi_path = dmc.get_result_path_prefix(1, 1, 1) + '99-psi-results.txt'
    sum_path = dmc.get_result_path_prefix(1, 1, 1) + '99-posterior-summary.txt'
    psis = get_values_psi_path(psi_path)
    omega, omega_hpd = get_omega_from_summary_path(sum_path)
    if cfg.div_model_prior == 'dpp':
        num_div_prior_psis, div_model_prior_psis = get_dpp_prior_values(
                config_path = config_path,
                num_samples = num_samples)
    elif cfg.div_model_prior == 'uniform':
        num_div_prior_psis, div_model_prior_psis = get_uniform_prior_values(
                npairs = npairs,
                num_samples = 10000)
    elif cfg.div_model_prior == 'psi':
        num_div_prior_psis, div_model_prior_psis = get_psi_uniform_prior_values(
                npairs = npairs,
                num_samples = 10000)

    bins = range(1, npairs + 2)

    hds = []
    for p in [psis, num_div_prior_psis, div_model_prior_psis]:
        hds.append(HistData(x = p,
                normed = True,
                bins = bins,
                histtype = 'bar',
                align = 'mid',
                orientation = 'vertical',
                zorder = 0))

    tick_labels = []
    for x in bins[0:-1]:
        if x % 2:
            tick_labels.append(str(x))
        else:
            tick_labels.append('')
    xticks_obj = Ticks(ticks = bins,
            labels = tick_labels,
            horizontalalignment = 'left',
            size = 8.0)
    hists = []
    for i, hd in enumerate(hds):
        right_text = ''
        if i == 0:
            right_text = r'$D_T = {0:.2f} ({1:.2f}-{2:.2f})$'.format(omega,
                    omega_hpd[0],
                    omega_hpd[1])
        hist = ScatterPlot(hist_data_list = [hd],
                # x_label = 'Number of divergence events',
                # y_label = 'Posterior probability',
                right_text = right_text,
                xticks_obj = xticks_obj)
        hist.set_xlim(left = bins[0], right = bins[-1])
        hist.set_ylim(bottom = 0.0, top = 0.45)
        hist.right_text_size = 10.0
        hist.plot_label_size = 12.0
        yticks = [i for i in hist.ax.get_yticks()]
        ytick_labels = [i for i in yticks]
        if len(ytick_labels) > 5:
            for i in range(1, len(ytick_labels), 2):
                ytick_labels[i] = ''
        yticks_obj = Ticks(ticks = yticks,
                labels = ytick_labels,
                size = 10.0)
        hist.yticks_obj = yticks_obj
        hists.append(hist)
    return hists

def create_plots(
        dpp_config_path,
        uniform_config_path,
        old_config_path,
        dpp_info_path,
        dpp_simple_info_path,
        dpp_inform_info_path,
        uniform_info_path,
        old_info_path,
        out_dir):
    # matplotlib.rc('text',**{'usetex': True})
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    dpp_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_info_path,
            num_samples = 1000000)
    dpp_simple_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_simple_info_path,
            num_samples = 1000000)
    dpp_inform_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_inform_info_path,
            num_samples = 1000000)
    uniform_hists = get_histograms(config_path = uniform_config_path,
            info_path = uniform_info_path,
            num_samples = 100000)
    old_hists = get_histograms(config_path = old_config_path,
            info_path = old_info_path,
            num_samples = 100000)

    hists = []
    # for i in range(len(dpp_hists)):
    for i in range(len(dpp_hists)):
        hists.append(old_hists[i])
        hists.append(uniform_hists[i])
        hists.append(dpp_hists[i])
        hists.append(dpp_inform_hists[i])
        hists.append(dpp_simple_hists[i])

    column_labels = [r'$msBayes$', r'$Uniform$', r'$DPP_{ }$', r'$DPP_{inform}$', r'$DPP_{simple}$']
    row_labels = ['Posterior', 'Prior', r'$p(M_{|\tau|, i})$']

    pg = PlotGrid(subplots = hists,
            num_columns = 5,
            share_x = True,
            share_y = True,
            height = 5.7,
            width = 11.0,
            auto_height = False,
            title = r'Number of divergence events, $|\tau|$',
            title_top = False,
            y_title = 'Probability',
            column_labels = column_labels,
            column_label_offset = 0.17,
            row_labels = row_labels,
            row_label_offset = 0.08)
    pg.auto_adjust_margins = False
    pg.margin_top = 0.915
    pg.margin_bottom = 0.04
    pg.margin_right = 0.965
    pg.padding_between_vertical = 1.0
    pg.reset_figure()
    pg.set_shared_x_limits()
    pg.set_shared_y_limits()
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-psi.pdf'))


def main_cli():
    create_plots( 
            dpp_config_path = project_util.PHILIPPINES_DPP_CFG,
            uniform_config_path = project_util.PHILIPPINES_UNIFORM_CFG,
            old_config_path = project_util.PHILIPPINES_OLD_CFG,
            dpp_info_path = project_util.PHILIPPINES_DPP_INFO,
            dpp_simple_info_path = project_util.PHILIPPINES_DPP_SIMPLE_INFO,
            dpp_inform_info_path = project_util.PHILIPPINES_DPP_INFORM_INFO,
            uniform_info_path = project_util.PHILIPPINES_UNIFORM_INFO,
            old_info_path = project_util.PHILIPPINES_OLD_INFO,
            out_dir = project_util.PLOT_DIR)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
        GLOBAL_RNG.seed(seed)
    main_cli()

