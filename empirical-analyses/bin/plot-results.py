#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults, spreadsheet_iter
from pymsbayes.config import MsBayesConfig
from pymsbayes.plotting import (Ticks, HistData, ScatterPlot, PlotGrid)
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def create_plots(info_path, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    dmc_sim = DMCSimulationResults(info_path)
    result_prefix = dmc_sim.get_result_path_prefix(1, 1, 1) + '99-'
    psi_path = result_prefix + 'psi-results.txt'
    psis = []
    for d in spreadsheet_iter([psi_path]):
        n = int(round(10000 * float(d['estimated_prob'])))
        psis.extend([int(d['num_of_div_events'])] * n)
    bins = range(1, dmc_sim.num_taxon_pairs + 2)
    hd = HistData(x = psis,
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
            y_label = 'Posterior probability')
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


def main_cli():
    create_plots(project_util.PHILIPPINES_DPP_INFO, project_util.PLOT_DIR)

if __name__ == '__main__':
    main_cli()

