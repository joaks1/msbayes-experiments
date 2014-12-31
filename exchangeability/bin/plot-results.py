#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting

def main_cli():
    bin_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.abspath(os.path.dirname(bin_dir))
    result_dir = os.path.abspath(os.path.join(project_dir, 'results'))
    info_path = os.path.join(result_dir, 'sort', 'pymsbayes-results',
            'pymsbayes-info.txt')
    plot_dir = os.path.join(result_dir, 'sort', 'pymsbayes-results',
            'plots')
    plotting.plot_validation_results(info_path,
            omega_symbol = r'D_T',
            psi_symbol = r'|\mathbf{\tau}|',
            mean_time_symbol = r'\bar{T}',
            math_font = None)
    vr = plotting.plot_validation_results(info_path,
            omega_symbol = r'D_T',
            psi_symbol = r'|\mathbf{\tau}|',
            mean_time_symbol = r'\bar{T}',
            label_schema = None,
            prob_plot_height = 3.4,
            prob_plot_margin_left = 0.005,
            prob_plot_margin_bottom = 0.005,
            prob_plot_margin_right = 1,
            prob_plot_margin_top = 1,
            plot_accuracy = False,
            prob_plot_glm = False,
            write_plots = False,
            math_font = None)
    vr['prior']['prior'].prob_plot.subplots[0].set_xlabel(
            xlabel = 'Estimated probability of one divergence')
    vr['prior']['prior'].save_prob_plot(os.path.join(plot_dir,
            'mc-unadjusted.pdf'))

if __name__ == '__main__':
    main_cli()

