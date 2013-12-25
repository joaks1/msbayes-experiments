#! /usr/bin/env python

import os
import sys

import matplotlib

from pymsbayes import teams, plotting
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

def get_ordered_divergence_model_probs(num_divergence_probs):
    part = stats.Partition([0] * len(num_divergence_probs))
    div_model_probs = {}
    for k, p in num_divergence_probs.iteritems():
        div_model_probs[k] = p / float(part.number_of_partitions_into_k_subsets(k))
    return div_model_probs

def get_dpp_prior_probs(config_path, num_samples = 100000):
    prob_team = teams.ModelProbabilityEstimatorTeam(
            config_paths = [config_path],
            num_samples = num_samples,
            num_processors = 8)
    prob_team.start()
    num_div_probs = prob_team.psi_probs[config_path]
    div_model_probs = get_divergence_model_probs(num_div_probs)
    ordered_div_model_probs = get_ordered_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs, ordered_div_model_probs

def get_dpp_prior_values(config_path, num_samples = 100000):
    num_div_probs, div_model_probs, ordered_div_model_probs = get_dpp_prior_probs(
            config_path,
            num_samples)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples),
            get_values_from_probs(ordered_div_model_probs, num_samples))

def get_uniform_prior_probs(npairs):
    ips = stats.IntegerPartition.number_of_int_partitions_by_k(
            num_elements = npairs)
    n = sum(ips)
    num_div_probs = {}
    for i in range(1, npairs + 1):
        num_div_probs[i] = ips[i-1] / float(n)
    div_model_probs = get_divergence_model_probs(num_div_probs)
    ordered_div_model_probs = get_ordered_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs, ordered_div_model_probs

def get_uniform_prior_values(npairs, num_samples = 10000):
    num_div_probs, div_model_probs, ordered_div_model_probs = get_uniform_prior_probs(npairs)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples),
            get_values_from_probs(ordered_div_model_probs, num_samples))

def get_psi_uniform_prior_probs(npairs):
    num_div_probs = {}
    for i in range(1, npairs + 1):
        num_div_probs[i] = 1.0 / npairs
    div_model_probs = get_divergence_model_probs(num_div_probs)
    ordered_div_model_probs = get_ordered_divergence_model_probs(num_div_probs)
    return num_div_probs, div_model_probs, ordered_div_model_probs

def get_psi_uniform_prior_values(npairs, num_samples = 10000):
    num_div_probs, div_model_probs, ordered_div_model_probs = get_psi_uniform_prior_probs(npairs)
    return (get_values_from_probs(num_div_probs, num_samples),
            get_values_from_probs(div_model_probs, num_samples),
            get_values_from_probs(ordered_div_model_probs, num_samples))

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
    total = sum(probs.itervalues())
    diff = 1.0 - total
    v = []
    for k, p in probs.iteritems():
        n = int(round(num_samples * p))
        v.extend([k] * n)
    n = int(round(num_samples * diff))
    v.extend([0] * n)
    return v

def get_values_psi_path(psi_path, num_samples = 10000):
    probs = get_probs_from_psi_path(psi_path)
    return get_values_from_probs(probs, num_samples)

def get_histograms(config_path,
        info_path,
        num_samples = 10000,
        num_div_values = None,
        div_model_values = None,
        ordered_div_model_values = None,
        iteration_index = 99,
        y_limits = [0.45, 0.45, 0.05, 0.05],
        xtick_label_size = 8.0):
    cfg = MsBayesConfig(config_path)
    dmc = DMCSimulationResults(info_path)
    npairs = dmc.num_taxon_pairs

    psi_path = (dmc.get_result_path_prefix(1, 1, 1) + 
            '{0}-psi-results.txt'.format(iteration_index))
    sum_path = (dmc.get_result_path_prefix(1, 1, 1) + 
            '{0}-posterior-summary.txt'.format(iteration_index))
    psis = get_values_psi_path(psi_path)
    omega, omega_hpd = get_omega_from_summary_path(sum_path)
    (num_div_prior_psis, div_model_prior_psis, ordered_div_model_prior_psis) = (
            num_div_values, div_model_values, ordered_div_model_values)
    if ((not num_div_values) or (not div_model_values) or
            (not ordered_div_model_values)):
        if cfg.div_model_prior == 'dpp':
            num_div_prior_psis, div_model_prior_psis, ordered_div_model_prior_psis = get_dpp_prior_values(
                    config_path = config_path,
                    num_samples = num_samples)
        elif cfg.div_model_prior == 'uniform':
            num_div_prior_psis, div_model_prior_psis, ordered_div_model_prior_psis = get_uniform_prior_values(
                    npairs = npairs,
                    num_samples = num_samples)
        elif cfg.div_model_prior == 'psi':
            num_div_prior_psis, div_model_prior_psis, ordered_div_model_prior_psis = get_psi_uniform_prior_values(
                    npairs = npairs,
                    num_samples = num_samples)

    # Extra bin for zero values
    bins = range(0, npairs + 2)

    hds = []
    for p in [psis, num_div_prior_psis, div_model_prior_psis, ordered_div_model_prior_psis]:
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
            size = xtick_label_size)
    hists = []
    for i, hd in enumerate(hds):
        right_text = ''
        if i == 0:
            right_text = r'$D_T = {0:.2f} ({1:.2f}-{2:.2f})$'.format(omega,
                    omega_hpd[0],
                    omega_hpd[1])
        hist = ScatterPlot(hist_data_list = [hd],
                right_text = right_text,
                xticks_obj = xticks_obj)
        # cut off extra zero-valued bin
        hist.set_xlim(left = bins[1], right = bins[-1])
        top = y_limits[i]
        hist.set_ylim(bottom = 0.0, top = top)
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
    dpp_num_div_values, dpp_div_model_values, dpp_ordered_model_values = get_dpp_prior_values(
                    config_path = dpp_config_path,
                    num_samples = 1000000)
    dpp_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_info_path,
            num_div_values = dpp_num_div_values,
            div_model_values = dpp_div_model_values,
            ordered_div_model_values = dpp_ordered_model_values)
    dpp_simple_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_simple_info_path,
            num_div_values = dpp_num_div_values,
            div_model_values = dpp_div_model_values,
            ordered_div_model_values = dpp_ordered_model_values)
    dpp_inform_hists = get_histograms(config_path = dpp_config_path,
            info_path = dpp_inform_info_path,
            num_div_values = dpp_num_div_values,
            div_model_values = dpp_div_model_values,
            ordered_div_model_values = dpp_ordered_model_values)
    uniform_hists = get_histograms(config_path = uniform_config_path,
            info_path = uniform_info_path,
            num_samples = 100000)
    old_hists = get_histograms(config_path = old_config_path,
            info_path = old_info_path,
            num_samples = 100000)

    hists = []
    for i in range(len(dpp_hists)):
        hists.append(old_hists[i])
        hists.append(uniform_hists[i])
        hists.append(dpp_hists[i])
        hists.append(dpp_inform_hists[i])
        hists.append(dpp_simple_hists[i])

    column_labels = [r'$\mathbf{M}_{msBayes}$', r'$\mathbf{M}_{Uniform}$', r'$\mathbf{M}_{DPP_{ }}$', r'$\mathbf{M}^{inform}_{DPP}$', r'$\mathbf{M}^{simple}_{DPP}$']
    row_labels = ['Posterior', 'Prior', r'Prior $\mathbb{E}(p(\mathbf{t}))$', r'Prior $\mathbb{E}(p(\mathbf{t^{\circ}}))$']

    pg = PlotGrid(subplots = hists,
            num_columns = 5,
            share_x = True,
            share_y = False,
            height = 7.2,
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
    pg.margin_top = 0.93
    pg.margin_bottom = 0.04
    pg.margin_right = 0.965
    pg.padding_between_vertical = 1.0
    pg.reset_figure()
    pg.set_shared_x_limits()
    pg.set_shared_y_limits(by_row = True)
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-psi.pdf'))

def create_negros_panay_plots(
        config_path,
        ordered_info_path,
        unordered_info_path,
        out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    dpp_num_div_values, dpp_div_model_values, dpp_ordered_model_values = get_dpp_prior_values(
                    config_path = config_path,
                    num_samples = 1000000)
    ordered_hists = get_histograms(config_path = config_path,
            info_path = ordered_info_path,
            num_div_values = dpp_num_div_values,
            div_model_values = dpp_div_model_values,
            ordered_div_model_values = dpp_ordered_model_values,
            iteration_index = 249,
            y_limits = [0.25, 0.25, 0.15, 0.15],
            xtick_label_size = 11.0)
    unordered_hists = get_histograms(config_path = config_path,
            info_path = unordered_info_path,
            num_div_values = dpp_num_div_values,
            div_model_values = dpp_div_model_values,
            ordered_div_model_values = dpp_ordered_model_values,
            iteration_index = 249,
            y_limits = [0.25, 0.25, 0.15, 0.15],
            xtick_label_size = 11.0)

    hists = [unordered_hists[0]] + ordered_hists

    row_labels = [r'Posterior $\mathbb{M}_{DPP}$', r'Posterior $\mathbb{M}^{\circ}_{DPP}$', 'Prior', r'Prior $\mathbb{E}(p(\mathbf{t}))$', r'Prior $\mathbb{E}(p(\mathbf{t^{\circ}}))$']

    pg = PlotGrid(subplots = hists,
            num_columns = 1,
            share_x = True,
            share_y = False,
            height = 7.2,
            width = 2.5,
            auto_height = False,
            title = r'Number of divergences, $|\tau|$',
            title_top = False,
            title_size = 10.0,
            y_title = 'Probability',
            row_labels = row_labels,
            row_label_offset = 0.08,
            row_label_size = 12.0)
    pg.auto_adjust_margins = False
    pg.margin_top = 0.98
    pg.margin_bottom = 0.03
    pg.margin_right = 0.88
    pg.margin_left = 0.05
    pg.padding_between_vertical = 1.0
    pg.reset_figure()
    pg.set_shared_x_limits()
    pg.set_shared_y_limits(by_row = True)
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'negros-panay-psi.pdf'))

def create_time_plot(config_path,
        info_path,
        out_dir,
        iteration_index = 249):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    cfg = MsBayesConfig(config_path)
    dmc = DMCSimulationResults(info_path)
    sum_path = (dmc.get_result_path_prefix(1, 1, 1) + 
            '{0}-posterior-summary.txt'.format(iteration_index))
    labels = []
    for t in cfg.taxa:
        l = t.strip().split('.')
        labels.append(r'\textit{{{0} {1}}}'.format(l[0], l[1]))
    pg = plotting.get_marginal_divergence_time_plot(
            config_path = config_path,
            posterior_summary_path = sum_path,
            labels = labels,
            label_size = 12.0,
            x_tick_label_size = 12.0,
            x_label_size = 16.0,
            y_label_size = 16.0)
    pg.savefig(os.path.join(out_dir, 'negros-panay-marginal-times.pdf'))

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
    create_negros_panay_plots(
            config_path = project_util.NEGROS_PANAY_CFG,
            ordered_info_path = project_util.NP_DPP_ORDERED_INFO,
            unordered_info_path = project_util.NP_DPP_UNORDERED_INFO,
            out_dir = project_util.PLOT_DIR)
    create_time_plot(
            config_path = project_util.NEGROS_PANAY_CFG,
            info_path = project_util.NP_DPP_ORDERED_INFO,
            out_dir = project_util.PLOT_DIR)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
        GLOBAL_RNG.seed(seed)
    main_cli()

