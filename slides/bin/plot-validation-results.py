#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
import project_util

def main_cli():
    results = {}
    for d in ['dpp', 'old', 'uniform', 'u-shaped']:
        info_path = os.path.join(project_util.VALIDATION_RESULT_DIR, d,
                    'pymsbayes-results', 'pymsbayes-info.txt')
        r = plotting.plot_validation_results(info_path,
                plot_dir = project_util.IMAGE_DIR,
                omega_symbol = r'D_T',
                psi_symbol = r'|\mathbf{\tau}|',
                mean_time_symbol = r'\bar{T}',
                plot_accuracy = False,
                prob_plot_glm = False,
                prob_plot_height = 3.5,
                prob_plot_margin_left = 0,
                prob_plot_margin_bottom = 0,
                prob_plot_margin_right = 1,
                prob_plot_margin_top = 0.975,
                prob_plot_padding_between_horizontal = 0.5,
                prob_plot_padding_between_vertical = 1.0,
                math_font = None,
                write_plots = False)
        for obs_name, p_dict in r.iteritems():
            for prior_name, validation_result in p_dict.iteritems():
                if not results.has_key(obs_name):
                    results[obs_name] = {}
                if not results[obs_name].has_key(prior_name):
                    results[obs_name][prior_name] = validation_result
                else:
                    raise Exception('Unexpected duplicate validation result')

    sub_plots = {}
    for i in ['old', 'dpp', 'uniform', 'u-shaped']:
        if not sub_plots.has_key(i):
            sub_plots[i] = {}
        for j in ['old', 'dpp', 'uniform', 'u-shaped']:
            sub_plots[i][j] = results['prior-' + i]['prior-' + j].prob_plot.subplots[0]
            sub_plots[i][j].set_xlabel('')
            sub_plots[i][j].set_ylabel('')

    sub_plot_list = [
            sub_plots['old']['old'],
            sub_plots['dpp']['old'],
            sub_plots['old']['dpp'],
            sub_plots['dpp']['dpp'],
            ]
    
    pg = plotting.PlotGrid(subplots = sub_plot_list[:1],
            num_columns = 1,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 14.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.001,
            y_title_size = 14.0,
            column_labels = [r'msBayes'],
            column_label_size = 22.0,
            column_label_offset = 0.04,
            width = 4.6,
            height = 3.7,
            auto_height = False)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.06
    pg.margin_left = 0.05
    pg.margin_top = 0.91
    pg.margin_right = 0.94
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-old.pdf')

    pg = plotting.PlotGrid(subplots = sub_plot_list[-1:],
            num_columns = 1,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 14.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.001,
            y_title_size = 14.0,
            column_labels = [r'dpp-msbayes'],
            column_label_size = 22.0,
            column_label_offset = 0.04,
            width = 4.6,
            height = 3.7,
            auto_height = False)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.06
    pg.margin_left = 0.05
    pg.margin_top = 0.91
    pg.margin_right = 0.94
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-dpp.pdf')

    pg = plotting.PlotGrid(subplots = sub_plot_list,
            num_columns = 2,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 16.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.03,
            y_title_size = 16.0,
            height = 6.0,
            auto_height = False,
            column_labels = [r'$M_{msBayes}$', r'$M_{DPP}$'],
            row_labels = [r'$M_{msBayes}$', r'$M_{DPP}$'],
            column_label_size = 22.0,
            row_label_size = 22.0,
            column_label_offset = 0.05,
            row_label_offset = 0.05,
            super_title = r'\textbf{Data model}',
            super_y_title = r'\textbf{Analysis model}',
            super_title_size = 20.0,
            super_y_title_size = 20.0,
            super_y_title_right = True)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.05
    pg.margin_left = 0.07
    pg.margin_top = 0.90
    pg.margin_right = 0.92
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-old-dpp.pdf')

    sub_plot_list = [
            sub_plots['old']['old'],
            sub_plots['dpp']['old'],
            sub_plots['uniform']['old'],
            sub_plots['u-shaped']['old'],
            sub_plots['old']['dpp'],
            sub_plots['dpp']['dpp'],
            sub_plots['uniform']['dpp'],
            sub_plots['u-shaped']['dpp'],
            ]
    for p in sub_plot_list:
        p.set_extra_y_label('')

    pg = plotting.PlotGrid(subplots = sub_plot_list,
            num_columns = 4,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 16.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.015,
            y_title_size = 16.0,
            height = 4.8,
            width = 11.0,
            auto_height = False,
            row_labels = [r'$M_{msBayes}$', r'$M_{DPP}$'],
            column_labels = [r'$M_{msBayes}$', r'$M_{DPP}$', r'$M_{Uniform}$', r'$M_{Ushaped}$'],
            column_label_size = 22.0,
            row_label_size = 22.0,
            column_label_offset = 0.05,
            row_label_offset = 0.05,
            super_title = r'\textbf{Data model}',
            super_y_title = r'\textbf{Analysis model}',
            super_title_size = 20.0,
            super_y_title_size = 20.0,
            super_y_title_right = True)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.06
    pg.margin_left = 0.045
    pg.margin_top = 0.88
    pg.margin_right = 0.94
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-old-dpp-full.pdf')

    for p in sub_plot_list:
        p.set_extra_y_label('')
        p.set_title_text('')

    old_violations = sub_plot_list[1:3]
    dpp_violations = sub_plot_list[4:5] + sub_plot_list[6:7]

    pg = plotting.PlotGrid(subplots = old_violations,
            num_columns = 1,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 16.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.015,
            y_title_size = 16.0,
            height = 6.5,
            width = 4.5,
            auto_height = False,
            column_labels = [r'msBayes'],
            column_label_size = 22.0,
            column_label_offset = 0.05,
            # super_title = r'\textbf{Data model}',
            # super_y_title = r'\textbf{Analysis model}',
            super_title_size = 20.0,
            super_y_title_size = 20.0,
            super_y_title_right = True)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.05
    pg.margin_left = 0.07
    pg.margin_top = 0.94
    pg.margin_right = 0.95
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-old-violations.pdf')

    pg = plotting.PlotGrid(subplots = dpp_violations,
            num_columns = 1,
            share_x = True,
            share_y = True,
            title = 'Posterior probability of one divergence',
            title_size = 16.0,
            title_top = False,
            y_title = 'True probability of one divergence',
            y_title_position = 0.015,
            y_title_size = 16.0,
            height = 6.5,
            width = 4.5,
            auto_height = False,
            column_labels = [r'dpp-msbayes'],
            column_label_size = 22.0,
            column_label_offset = 0.05,
            # super_title = r'\textbf{Data model}',
            # super_y_title = r'\textbf{Analysis model}',
            super_title_size = 20.0,
            super_y_title_size = 20.0,
            super_y_title_right = True)
    pg.label_schema = None
    pg.auto_adjust_margins = False
    pg.margin_bottom = 0.05
    pg.margin_left = 0.07
    pg.margin_top = 0.94
    pg.margin_right = 0.95
    pg.reset_figure()

    pg.savefig('../images/validation-model-choice-dpp-violations.pdf')

if __name__ == '__main__':
    main_cli()

