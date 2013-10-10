#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
import project_util

def main_cli():
    for d in ['dpp', 'old']:
        info_path = os.path.join(project_util.VALIDATION_RESULT_DIR, d,
                    'pymsbayes-results', 'pymsbayes-info.txt')
        plotting.plot_validation_results(info_path,
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
                math_font = None)

if __name__ == '__main__':
    main_cli()

