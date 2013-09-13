#! /usr/bin/env python

import os
import sys
import re

from pymsbayes import plotting
from pymsbayes.utils.parsing import parse_posterior_summary_file
from pymsbayes.fileio import process_file_arg
import project_util

def main_cli():
    sum_file_pattern = re.compile(
            r'^d1-m1-s1-(?P<iter_index>\d{1,4})-posterior-summary.txt.gz$')
    result_dir = os.path.join(project_util.RESULT_DIR, 'sampling-error',
            'pymsbayes-results')
    post_dir = os.path.join(result_dir, 'pymsbayes-output',
            'd1', 'm1')
    post_sum_paths  = {}
    for f in os.listdir(post_dir):
        m = sum_file_pattern.match(f)
        if m:
            post_sum_paths[int(m.group('iter_index'))] = os.path.join(post_dir,
                    f)
    iter_indices = sorted(post_sum_paths.iterkeys())
    nsamples = []
    omega_HPD_low = []
    omega_HPD_high = []
    omega_HPD_low_glm = []
    omega_HPD_high_glm = []
    for i in iter_indices:
        nsamples.append((i + 1) * 100000)
        f, close = process_file_arg(post_sum_paths[i], 'r')
        post_sum = parse_posterior_summary_file(f)
        hpd_int  = post_sum['PRI.omega']['HPD_95_interval']
        omega_HPD_low.append(float(hpd_int[0]))
        omega_HPD_high.append(float(hpd_int[1]))
        hpd_int_glm  = post_sum['PRI.omega']['HPD_95_interval_glm']
        omega_HPD_low_glm.append(float(hpd_int_glm[0]))
        omega_HPD_high_glm.append(float(hpd_int_glm[1]))
        f.close()

    sp_list = []
    sd_list = []
    sd_list.append(plotting.ScatterData(x = nsamples, y = omega_HPD_low))
    sd_list.append(plotting.ScatterData(x = nsamples, y = omega_HPD_high))
    sp = plotting.ScatterPlot(
            scatter_data_list = sd_list,
            y_label = r'$\Omega$  95% HPD')
    sp_list.append(sp)

    sd_list = []
    sd_list.append(plotting.ScatterData(x = nsamples, y = omega_HPD_low_glm))
    sd_list.append(plotting.ScatterData(x = nsamples, y = omega_HPD_high_glm))
    sp = plotting.ScatterPlot(
            scatter_data_list = sd_list,
            y_label = r'$\Omega$  95% HPD (GLM-adjusted)')
    sp_list.append(sp)

    pg = plotting.PlotGrid(subplots = sp_list,
            num_columns = 1,
            title = r'Number of prior samples',
            title_top = False,
            share_x = True,
            share_y = False,
            width = 8.0,
            height = 10.0,
            auto_height = False)
    pg.auto_adjust_margins = False
    pg.margin_top = 0.99
    pg.margin_bottom = 0.01
    pg.reset_figure()

    pg.savefig(os.path.join(result_dir, 'omega_over_sampling.pdf'))

if __name__ == '__main__':
    main_cli()

