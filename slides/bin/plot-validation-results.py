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
            print sub_plots[i][j]

if __name__ == '__main__':
    main_cli()

