#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
import project_util

def main_cli():
    info_path = os.path.join(project_util.NO_SORT_DIR, 'results',
                'pymsbayes-results', 'pymsbayes-info.txt')
    plotting.plot_validation_results(info_path,
            omega_symbol = r'D_T',
            psi_symbol = r'|\mathbf{\tau}|',
            mean_time_symbol = r'\bar{T}',
            math_font = None)

if __name__ == '__main__':
    main_cli()

