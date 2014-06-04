#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting

def main_cli():
    bin_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.abspath(os.path.dirname(bin_dir))
    result_dir = os.path.abspath(os.path.join(project_dir, 'results'))
    info_path = os.path.join(result_dir, 'multi-locus-no-sort', 'pymsbayes-results',
            'pymsbayes-info.txt')
    plotting.plot_validation_results(info_path,
            omega_symbol = r'D_T',
            psi_symbol = r'|\mathbf{\tau}|',
            mean_time_symbol = r'\bar{T}',
            math_font = None)

if __name__ == '__main__':
    main_cli()

