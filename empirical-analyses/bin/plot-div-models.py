#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
from pymsbayes.utils import parsing
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)

def get_div_model_result_path(dmc_sim_result, iteration_index):
    path = (dmc_sim_result.get_result_path_prefix(1,1,1) + 
            '{0}-div-model-results.txt'.format(iteration_index))
    return path

def get_posterior_path(dmc_sim_result, iteration_index):
    path = (dmc_sim_result.get_result_path_prefix(1,1,1) + 
            '{0}-posterior-sample.txt.gz'.format(iteration_index))
    return path

def get_div_model_plot_grid(
        info_path,
        iteration_index = 99,
        ordered = False,
        margin_top = 0.99,
        padding_between_vertical = 0.8):
    dmc = parsing.DMCSimulationResults(info_path)
    div_model_path = get_div_model_result_path(dmc, iteration_index)
    if ordered:
        div_model_path = get_posterior_path(dmc, iteration_index)
    p = plotting.UnorderedDivergenceModelPlotGrid(
            div_model_results_path = div_model_path,
            num_top_models = 10,
            height = 10.0,
            width = 8.0,
            data_label_size = 10.0,
            plot_label_schema = 'uppercase',
            plot_label_offset = 0,
            plot_label_size = 12.0,
            y_title = 'Divergence time',
            y_title_size = 14.0,
            y_tick_label_size = 10.0,
            right_text_size = 10.0,
            margin_left = 0.03,
            margin_bottom = 0.0,
            margin_right = 1,
            margin_top = margin_top,
            padding_between_vertical = padding_between_vertical)
    return p.create_grid()

def main_cli():
    pg = get_div_model_plot_grid(
            info_path = project_util.PHILIPPINES_DPP_INFO,
            iteration_index = 99)
    path = os.path.join(project_util.PLOT_DIR, 'philippines-dpp-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.PHILIPPINES_DPP_INFORM_INFO,
            iteration_index = 99)
    path = os.path.join(project_util.PLOT_DIR, 'philippines-dpp-inform-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.PHILIPPINES_DPP_SIMPLE_INFO,
            iteration_index = 99)
    path = os.path.join(project_util.PLOT_DIR, 'philippines-dpp-simple-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.PHILIPPINES_UNIFORM_INFO,
            iteration_index = 99,
            margin_top = 0.985,
            padding_between_vertical = 0.9)
    path = os.path.join(project_util.PLOT_DIR, 'philippines-uniform-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.PHILIPPINES_OLD_INFO,
            iteration_index = 99,
            margin_top = 0.985,
            padding_between_vertical = 0.9)
    path = os.path.join(project_util.PLOT_DIR, 'philippines-old-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.NP_DPP_UNORDERED_INFO,
            iteration_index = 249)
    path = os.path.join(project_util.PLOT_DIR, 'negros-panay-dpp-unordered-div-models.pdf')
    pg.savefig(path)

    pg = get_div_model_plot_grid(
            info_path = project_util.NP_DPP_ORDERED_INFO,
            iteration_index = 249,
            ordered = True)
    path = os.path.join(project_util.PLOT_DIR, 'negros-panay-dpp-ordered-div-models.pdf')
    pg.savefig(path)

if __name__ == '__main__':
    main_cli()

