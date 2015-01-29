#! /usr/bin/env python

import os
import sys

import matplotlib

from pymsbayes import plotting
from pymsbayes.utils import stats
from pymsbayes.utils.messaging import get_logger

import project_util

_LOG = get_logger(__name__)

def get_ordered_divergence_model_numbers(num_pairs):
    part = stats.Partition([0] * num_pairs)
    prob_div_models = []
    num_div_models = [part.number_of_partitions_into_k_subsets(i+1) for i in range(num_pairs)]
    prob_div_models = [((1.0 / num_pairs) / x) for x in num_div_models]
    return num_div_models, prob_div_models

def get_unordered_divergence_model_numbers(num_pairs):
    part = stats.IntegerPartition([0] * num_pairs)
    prob_div_models = []
    num_div_models = part.number_of_int_partitions_by_k(num_pairs)
    prob_div_models = [((1.0 / num_pairs) / x) for x in num_div_models]
    return num_div_models, prob_div_models

def create_plots(n = 22,
        ordered = True,
        x_label_size = 24.0,
        y_label_size = 24.0,
        xtick_label_size = 16.0,
        ytick_label_size = 14.0,
        height = 6.0,
        width = 8.0,
        margin_bottom = 0.0,
        margin_left = 0.0,
        margin_top = 1.0,
        margin_right = 1.0,
        padding_between_vertical = 1.0):

    if ordered:
        num_div_models, prob_div_models = get_ordered_divergence_model_numbers(n)
    else:
        num_div_models, prob_div_models = get_unordered_divergence_model_numbers(n)

    keys = [(i + 1) for i in range(n)] 
    num_bar_data = plotting.BarData(
                values = num_div_models,
                labels = keys,
                width = 1.0,
                orientation = 'vertical',
                color = '0.5',
                edgecolor = '0.5',
                label_size = xtick_label_size,
                measure_tick_label_size = ytick_label_size,
                zorder = 0)
    prob_bar_data = plotting.BarData(
                values = prob_div_models,
                labels = keys,
                width = 1.0,
                orientation = 'vertical',
                color = '0.5',
                edgecolor = '0.5',
                label_size = xtick_label_size,
                measure_tick_label_size = ytick_label_size,
                zorder = 0)
    ymax = 1.05 * max(num_div_models)
    num_plot = plotting.ScatterPlot(
                    bar_data_list = [num_bar_data],
                    x_label = '# of divergence events',
                    y_label = '# of divergence models',
                    x_label_size = x_label_size,
                    y_label_size = y_label_size,
                    ylim = (0, ymax),
                    )
    ymax = 1.05 * max(prob_div_models)
    prob_plot = plotting.ScatterPlot(
                    bar_data_list = [prob_bar_data],
                    x_label = '# of divergence events',
                    y_label = 'Prior probability',
                    x_label_size = x_label_size,
                    y_label_size = y_label_size,
                    ylim = (0, ymax),
                    )
    for p in [num_plot, prob_plot]:
        yticks = [i for i in p.ax.get_yticks()]
        ytick_labels = [i for i in yticks]
        if len(ytick_labels) > 5:
            for i in range(1, len(ytick_labels), 2):
                ytick_labels[i] = ''
        yticks_obj = plotting.Ticks(ticks = yticks,
                labels = ytick_labels,
                size = ytick_label_size)
        p.yticks_obj = yticks_obj

    # return num_plot, prob_plot
    num_grid = plotting.PlotGrid(subplots = [num_plot],
            label_schema = None,
            num_columns = 1,
            height = height,
            width = width,
            auto_height = False)
    prob_grid = plotting.PlotGrid(subplots = [prob_plot],
            label_schema = None,
            num_columns = 1,
            height = height,
            width = width,
            auto_height = False)
    for p in [num_grid, prob_grid]:
        p.auto_adjust_margins = False
        p.margin_top = margin_top
        p.margin_bottom = margin_bottom
        p.margin_right = margin_right
        p.margin_left = margin_left
        p.padding_between_vertical = padding_between_vertical
        p.reset_figure()
        p.reset_figure()
    return num_grid, prob_grid

if __name__ == '__main__':
    num_plot, prob_plot = create_plots(n = 22)

    num_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'number-of-div-models-22.pdf'))
    prob_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'prob-of-div-models-22.pdf'))

    num_plot, prob_plot = create_plots(n = 22, ordered = False)

    num_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'number-of-div-models-22-unordered.pdf'))
    prob_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'prob-of-div-models-22-unordered.pdf'))


    num_plot, prob_plot = create_plots(n = 10,
            ordered = True)

    num_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'number-of-div-models-10.pdf'))
    prob_plot.savefig(os.path.join(project_util.IMAGE_DIR, 'prob-of-div-models-10.pdf'))
