#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
import project_util

def main_cli():
    if not os.path.exists(project_util.IMAGE_DIR):
        os.mkdir(project_util.IMAGE_DIR)
    results = {}
    for d in ['dpp', 'old', 'uniform', 'u-shaped']:
        info_path = os.path.join(project_util.RESULT_DIR, d,
                    'pymsbayes-results', 'pymsbayes-info.txt')
        r = plotting.plot_validation_results(info_path,
                plot_dir = project_util.IMAGE_DIR,
                omega_symbol = r'D_T',
                psi_symbol = r'|\mathbf{\tau}|',
                mean_time_symbol = r'\bar{T}',
                plot_accuracy = True,
                prob_plot_glm = True,
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

    sub_plot_map = {
            0: ('psi',
                r'True number of divergence events, $|\mathbf{\tau}|$',
                r'Estimated number of divergence events, $\hat{|\mathbf{\tau}|}$ (mode)'),
            1: ('omega',
                r'True variance of divergence times, $D_T$',
                r'Estimated variance of divergence times, $\hat{D_T}$ (median)'),
            2: ('time',
                r'True mean of divergence times, $\bar{T}$',
                r'Estimated mean of divergence times, $\hat{\bar{T}}$ (median)'),
            3: ('psi-glm',
                r'True number of divergence events, $|\mathbf{\tau}|$',
                r'GLM-adjusted number of divergence events, $\hat{|\mathbf{\tau}|}$ (mode)'),
            4: ('omega-glm',
                r'True variance of divergence times, $D_T$',
                r'GLM-adjusted variance of divergence times, $\hat{D_T}$ (median)'),
            5: ('time-glm',
                r'True mean of divergence times, $\bar{T}$',
                r'GLM-adjusted mean of divergence times, $\hat{\bar{T}}$ (median)'),
                }
    for idx, (variable, x_label, y_label) in sub_plot_map.iteritems():
        sub_plots = {}
        for i in ['old', 'dpp', 'uniform', 'u-shaped']:
            if not sub_plots.has_key(i):
                sub_plots[i] = {}
            for j in ['old', 'dpp', 'uniform', 'u-shaped']:
                sub_plots[i][j] = results['prior-' + i]['prior-' + j].accuracy_plot.subplots[idx]
                sub_plots[i][j].set_xlabel('')
                sub_plots[i][j].set_ylabel('')

        sub_plot_list = [
                sub_plots['old']['old'],
                sub_plots['u-shaped']['old'],
                sub_plots['uniform']['old'],
                sub_plots['dpp']['old'],
                sub_plots['old']['u-shaped'],
                sub_plots['u-shaped']['u-shaped'],
                sub_plots['uniform']['u-shaped'],
                sub_plots['dpp']['u-shaped'],
                sub_plots['old']['uniform'],
                sub_plots['u-shaped']['uniform'],
                sub_plots['uniform']['uniform'],
                sub_plots['dpp']['uniform'],
                sub_plots['old']['dpp'],
                sub_plots['u-shaped']['dpp'],
                sub_plots['uniform']['dpp'],
                sub_plots['dpp']['dpp'],
                ]
        for p in sub_plot_list:
            p.set_extra_y_label('')
            for scatter_data in p.scatter_data_list:
                scatter_data.markersize = 5.0

        pg = plotting.PlotGrid(subplots = sub_plot_list,
                num_columns = 4,
                share_x = True,
                share_y = True,
                title = x_label,
                title_size = 14.0,
                title_top = False,
                y_title = y_label,
                y_title_position = 0.015,
                y_title_size = 14.0,
                height = 9.0,
                width = 11.0,
                auto_height = False,
                row_labels = [r'$M_{msBayes}$', r'$M_{Ushaped}$', r'$M_{Uniform}$', r'$M_{DPP}$'],
                column_labels = [r'$M_{msBayes}$', r'$M_{Ushaped}$', r'$M_{Uniform}$', r'$M_{DPP}$'],
                column_label_size = 20.0,
                row_label_size = 20.0,
                column_label_offset = 0.1,
                row_label_offset = 0.05,
                super_title = r'\textbf{Data model}',
                super_y_title = r'\textbf{Inference model}',
                super_title_size = 20.0,
                super_y_title_size = 20.0,
                super_y_title_right = True)
        # pg.label_schema = None
        pg.auto_adjust_margins = False
        pg.margin_bottom = 0.04
        pg.margin_left = 0.04
        pg.margin_top = 0.92
        pg.margin_right = 0.94
        pg.plot_label_size = 12.0
        pg.padding_between_vertical = 1.2
        pg.reset_figure()

        pg.set_shared_x_limits()
        pg.set_shared_y_limits()
        pg.reset_figure()

        pg.savefig(os.path.join(project_util.IMAGE_DIR,
                'validation-accuracy-' + variable + '.pdf'))

if __name__ == '__main__':
    main_cli()

