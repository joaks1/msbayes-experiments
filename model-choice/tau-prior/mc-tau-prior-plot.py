#! /usr/bin/env python

import os
import sys

from pymsbayes.plotting import (HistData, ScatterPlot)
from pymsbayes.utils.messaging import get_logger

_LOG = get_logger(__name__)

def main_cli():
    taus = []
    unique_taus = []
    f = open('tau.txt', 'rU')
    f.next()
    for l in f:
        l = l.strip().split()
        taus.extend([float(t) for t in l])
        unique_taus.extend([float(t) for t in set(l)])
    hd_t = HistData(x = taus,
            bins=10,
            zorder = 0)
    plot_t = ScatterPlot(
            hist_data_list = [hd_t],
            x_label = r'Divergence time ($\tau$)',
            y_label = r'Density')
    plot_t.savefig('tau_prior.pdf')
    hd_t = HistData(x = unique_taus,
            bins=10,
            zorder = 0)
    plot_t = ScatterPlot(
            hist_data_list = [hd_t],
            x_label = r'Divergence time ($\tau$)',
            y_label = r'Density')
    plot_t.savefig('unique_tau_prior.pdf')

if __name__ == '__main__':
    main_cli()

