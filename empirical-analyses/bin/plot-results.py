#! /usr/bin/env python

import os
import sys

import matplotlib

from pymsbayes.utils.parsing import DMCSimulationResults, spreadsheet_iter
from pymsbayes.config import MsBayesConfig
from pymsbayes.plotting import (Ticks, HistData, ScatterPlot, PlotGrid)
from pymsbayes.utils.stats import Partition
from pymsbayes.utils.probability import GammaDistribution
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def get_dpp_psi_values(num_elements, shape, scale, num_sims = 100000):
    conc = GammaDistribution(shape, scale)
    p = Partition([1] * num_elements)
    psis = []
    for i in range(num_sims):
        a = conc.draw()
        x = p.dirichlet_process_draw(a)
        psis.append(len(set(x)))
    return psis

def create_plots(dpp_info_path, old_info_path, out_dir):
    # matplotlib.rc('text',**{'usetex': True})
    # old = ([1] * 992) + ([2] * 8)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    dmc_sim = DMCSimulationResults(dpp_info_path)
    dmc_sim_old = DMCSimulationResults(old_info_path)
    psi_path = dmc_sim.get_result_path_prefix(1, 1, 1) + '99-psi-results.txt'
    psi_path_old = dmc_sim_old.get_result_path_prefix(1, 1, 1) + '99-psi-results.txt'
    psis = []
    for d in spreadsheet_iter([psi_path]):
        n = int(round(10000 * float(d['estimated_prob'])))
        psis.extend([int(d['num_of_div_events'])] * n)
    psis_old = []
    for d in spreadsheet_iter([psi_path_old]):
        n = int(round(10000 * float(d['estimated_prob'])))
        psis_old.extend([int(d['num_of_div_events'])] * n)
    bins = range(1, dmc_sim.num_taxon_pairs + 2)
    hd = HistData(x = psis,
            normed = True,
            bins = bins,
            histtype = 'bar',
            align = 'mid',
            orientation = 'vertical',
            zorder = 0)
    # hd_old= HistData(x = old,
    hd_old= HistData(x = psis_old,
            normed = True,
            bins = bins,
            histtype = 'bar',
            align = 'mid',
            orientation = 'vertical',
            zorder = 0)
    tick_labels = []
    for x in bins[0:-1]:
        if x % 2:
            tick_labels.append(str(x))
        else:
            tick_labels.append('')
    xticks_obj = Ticks(ticks = bins,
            labels = tick_labels,
            horizontalalignment = 'left')
    hist = ScatterPlot(hist_data_list = [hd],
            x_label = 'Number of divergence events',
            y_label = 'Posterior probability',
            xticks_obj = xticks_obj)
    hist_old = ScatterPlot(hist_data_list = [hd_old],
            x_label = 'Number of divergence events',
            y_label = 'Posterior probability',
            xticks_obj = xticks_obj)
    hist.set_xlim(left = bins[0], right = bins[-1])
    hist_old.set_xlim(left = bins[0], right = bins[-1])
    hist.set_ylim(bottom = 0.0, top = 0.1)
    pg = PlotGrid(subplots = [hist],
            num_columns = 1,
            height = 4.0,
            width = 6.5,
            label_schema = None,
            auto_height = False)
    pg.auto_adjust_margins = False
    pg.margin_top = 1
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-dpp-psi-posterior.pdf'))

    # hist.set_ylim(bottom = 0.0, top = 1.0)
    hist.set_ylim(bottom = 0.0, top = 0.5)
    hist.set_ylabel('')
    # hist_old.set_ylim(bottom = 0.0, top = 1.0)
    hist_old.set_ylim(bottom = 0.0, top = 0.5)
    pg = PlotGrid(subplots = [hist_old, hist],
            num_columns = 2,
            height = 3.5,
            width = 8.0,
            share_x = True,
            share_y = True,
            label_schema = None,
            auto_height = False,
            # column_labels = [r'\texttt{msBayes}', r'\texttt{dpp-msbayes}'],
            column_labels = [r'msBayes', r'dpp-msbayes'],
            column_label_size = 18.0)
    pg.auto_adjust_margins = False
    pg.margin_top = 0.92
    pg.padding_between_horizontal = 1.0
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-dpp-psi-posterior-old-vs-dpp.pdf'))
    pg.label_schema = 'uppercase'
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-dpp-psi-posterior-old-vs-dpp-labels.pdf'))

    prior_psis = get_dpp_psi_values(dmc_sim.num_taxon_pairs, 1.5, 18.099702, num_sims = 100000)
    prior_hd = HistData(x = prior_psis,
            normed = True,
            bins = bins,
            histtype = 'bar',
            align = 'mid',
            orientation = 'vertical',
            zorder = 0)
    prior_hist = ScatterPlot(hist_data_list = [prior_hd],
            x_label = 'Number of divergence events',
            y_label = 'Probability',
            xticks_obj = xticks_obj)
    prior_hist.set_xlim(left = bins[0], right = bins[-1])
    prior_hist.set_ylim(bottom = 0.0, top = 0.12)
    hist.set_ylim(bottom = 0.0, top = 0.12)
    pg = PlotGrid(subplots = [prior_hist, hist],
            num_columns = 2,
            height = 3.5,
            width = 8.0,
            share_x = True,
            share_y = True,
            label_schema = None,
            auto_height = False,
            # column_labels = [r'\texttt{msBayes}', r'\texttt{dpp-msbayes}'],
            column_labels = [r'Prior', r'Posterior'],
            column_label_size = 18.0)
    pg.auto_adjust_margins = False
    pg.margin_top = 0.92
    pg.padding_between_horizontal = 1.0
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-dpp-psi-posterior-prior.pdf'))
    pg.label_schema = 'uppercase'
    pg.reset_figure()
    pg.savefig(os.path.join(out_dir, 'philippines-dpp-psi-posterior-prior-lablels.pdf'))


def main_cli():
    create_plots(project_util.PHILIPPINES_DPP_INFO, 
            project_util.PHILIPPINES_OLD_INFO,
            project_util.PLOT_DIR)

if __name__ == '__main__':
    main_cli()

