#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
import project_util

def main_cli():
    info_path = os.path.join(project_util.RESULT_DIR, 'validation', 'results',
                'pymsbayes-results', 'pymsbayes-info.txt')
    plotting.plot_model_choice_validation_results(info_path)

if __name__ == '__main__':
    main_cli()

