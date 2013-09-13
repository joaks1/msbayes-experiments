#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
from pymsbayes.utils.parsing import spreadsheet_iter
import project_util

def main_cli():
    for d in ['hickerson', 'alt']:
        result_dir = os.path.join(project_util.RESULT_DIR, d,
                'pymsbayes-results')
        post_sample_path = os.path.join(result_dir, 'pymsbayes-output',
                'd1', 'm12345678-combined',
                'd1-m12345678-combined-s1-25-posterior-sample.txt.gz')
        model_i = range(1, 9)
        mean_tau = dict(zip([i for i in model_i],[[] for i in model_i]))
        omega = dict(zip([i for i in model_i],[[] for i in model_i]))
        for d in spreadsheet_iter([post_sample_path]):
            model_index = (int(d['PRI.model']))
            mean_tau[model_index].append(float(d['PRI.E.t']))
            omega[model_index].append(float(d['PRI.omega']))

        scatter_data = {}
        xmin, xmax = 0., 0.
        ymin, ymax = 0., 0.
        for i in model_i:
            markeredgecolor = '0.5'
            if i in [5, 6]:
                markeredgecolor = '0.05'
            x = omega[i]
            y = mean_tau[i]
            sd = plotting.ScatterData(x = x, y = y,
                    markeredgecolor = markeredgecolor)
            scatter_data[i] = sd
            xmin = min([xmin] + x)
            ymin = min([ymin] + y)
            xmax = max([xmax] + x)
            ymax = max([ymax] + y)
        xbuff = (xmax - xmin) * 0.04
        ybuff = (ymax - ymin) * 0.04
        xlim = (xmin - xbuff, xmax + xbuff)
        ylim = (ymin - ybuff, ymax + ybuff)
        
        sp = plotting.ScatterPlot(
                scatter_data_list = scatter_data.values(),
                x_label = r'$Var(\tau)/E(\tau)$ ($\Omega$)',
                y_label = r'$E(\tau)$',
                xlim = xlim,
                ylim = ylim)
        rect = [0, 0, 1, 1]
        sp.fig.tight_layout(pad = 0.25, rect = rect)
        sp.reset_plot()
        sp.savefig(os.path.join(result_dir, 'mean_by_dispersion.pdf'))

if __name__ == '__main__':
    main_cli()

