#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
from pymsbayes.utils.parsing import spreadsheet_iter
from pymsbayes.fileio import process_file_arg
from pymsbayes.utils.stats import get_freqs, freq_less_than, median, mode_list
import project_util

def parse_results(posterior_path):
    omegas = []
    psis = []
    models = []
    for i, d in enumerate(spreadsheet_iter([posterior_path])):
        models.append(int(d['PRI.model']))
        omegas.append(float(d['PRI.omega']))
        psis.append(int(d['PRI.Psi']))
    return models, psis, omegas

def summarize_results(posterior_path):
    sum_path = posterior_path + '.summary.txt'
    models, psis, omegas = parse_results(posterior_path)
    psi_mode = mode_list(psis)
    omega_mode = mode_list(omegas)
    omega_median = median(omegas)
    psi_probs = get_freqs(psis)
    omega_prob = freq_less_than(omegas, 0.01)
    model_probs = get_freqs(models)
    with open(sum_path, 'w') as out:
        out.write('\nResults for {0!r}:\n'.format(posterior_path))
        out.write('psi_mode = {0}\n'.format(psi_mode))
        out.write('psi_probs = {0}\n'.format(psi_probs))
        out.write('omega_mode = {0}\n'.format(omega_mode))
        out.write('omega_median = {0}\n'.format(omega_median))
        out.write('omega_prob_less_than = {0}\n'.format(omega_prob))
        out.write('model_probs = {0}\n'.format(model_probs))

def rescale_posterior(in_path, out_path, scale_factor, model_indices):
    header = None
    out, close = process_file_arg(out_path, 'w', compresslevel=9)
    omegas = []
    psis = []
    for i, d in enumerate(spreadsheet_iter([in_path])):
        if i == 0:
            header = d.keys()
            out.write('{0}\n'.format('\t'.join(header)))
        model_index = int(d['PRI.model'])
        if model_index in model_indices:
            d['PRI.E.t'] = float(d['PRI.E.t']) * scale_factor
            d['PRI.var.t'] = float(d['PRI.var.t']) * (scale_factor * 0.5)
            d['PRI.omega'] = float(d['PRI.omega']) * scale_factor
            omegas.append(d['PRI.omega'])
            psis.append(int(d['PRI.Psi']))
        out.write('{0}\n'.format('\t'.join([
                str(d[k]) for k in d.iterkeys()])))
    out.close()
    return omegas, psis

def get_omega_and_mean_tau(post_path, model_indices):
    mean_tau = dict(zip([i for i in model_indices],[[] for i in model_indices]))
    omega = dict(zip([i for i in model_indices],[[] for i in model_indices]))
    for d in spreadsheet_iter([post_path]):
        model_index = (int(d['PRI.model']))
        mean_tau[model_index].append(float(d['PRI.E.t']))
        omega[model_index].append(float(d['PRI.omega']))
    return omega, mean_tau

def get_posterior_plot(post_path, model_indices, scaled_model_indices,
        xlim = None, ylim = None,
        x_label = r'$Var(\tau)/E(\tau)$ ($\Omega$)',
        y_label = r'$E(\tau)$'):
    omega, mean_tau = get_omega_and_mean_tau(post_path, model_indices)
    scatter_data = {}
    xmin, xmax = 0., 0.
    ymin, ymax = 0., 0.
    for i in model_indices:
        markeredgecolor = '0.5'
        if i in scaled_model_indices:
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
    if not xlim:
        xlim = (xmin - xbuff, xmax + xbuff)
    if not ylim:
        ylim = (ymin - ybuff, ymax + ybuff)
    
    sp = plotting.ScatterPlot(
            scatter_data_list = scatter_data.values(),
            x_label = x_label,
            y_label = y_label,
            xlim = xlim,
            ylim = ylim)
    return sp, xlim, ylim

def plot_posteriors(post_path, scaled_post_path, model_indices = range(1, 9),
        scaled_model_indices = [5, 6]):
    sp, xlim, ylim = get_posterior_plot(post_path, model_indices, scaled_model_indices,
            xlim = None,
            ylim = None,
            x_label = None)
    sp_scaled, xlim, ylim = get_posterior_plot(scaled_post_path, model_indices,
            scaled_model_indices,
            xlim = xlim,
            ylim = ylim,
            x_label = None,
            y_label = None)
    pg = plotting.PlotGrid(
            subplots = [sp, sp_scaled],
            num_columns = 2,
            share_x = True,
            share_y = True,
            title = r'$Var(\tau)/E(\tau)$ ($\Omega$)',
            title_top = False,
            width = 8.0,
            height = 3.5,
            auto_height = False)
    pg.auto_adjust_margins = False
    pg.margin_left = 0.0
    pg.margin_top = 0.96
    pg.margin_bottom = 0.06
    pg.reset_figure()
    return pg
    
def process_posterior(post_path, scaled_post_path):
    prior_prob_omega_less_than = 0.0887
    scaled_indices = [5, 6]
    omegas, psis = rescale_posterior(in_path = post_path,
            out_path = scaled_post_path,
            scale_factor = 0.4,
            model_indices = scaled_indices)
    summarize_results(scaled_post_path)

    model_indices = range(1, 9)
    pg = plot_posteriors(post_path, scaled_post_path, model_indices,
            scaled_indices)

    pg.savefig(os.path.join(os.path.dirname(post_path),
            'mean_by_dispersion_rescaled.pdf'))

def main_cli():
    # rescale posterior from Hickerson et al.
    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'hickerson-posterior-1k')
    post_sample_path = os.path.join(result_dir, 'posterior-from-mike-1k.txt.gz')
    scaled_post_path = os.path.join(result_dir,
            'rescaled-posterior-from-mike.txt.gz')
    process_posterior(post_sample_path, scaled_post_path)

    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'hickerson-posterior-10k')
    post_sample_path = os.path.join(result_dir, 'posterior-from-mike-10k.txt.gz')
    scaled_post_path = os.path.join(result_dir,
            'rescaled-posterior-from-mike.txt.gz')
    process_posterior(post_sample_path, scaled_post_path)

    # rescale posterior calculated via EuReject from Hickerson et al.
    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'eureject-results')
    post_sample_path = os.path.join(result_dir, 'posterior-sample.txt.gz')
    scaled_post_path = os.path.join(result_dir,
            'rescaled-posterior-sample.txt.gz')
    process_posterior(post_sample_path, scaled_post_path)

    # rescale re-analysis posteriors
    for d in ['hickerson', 'alt']:
        result_dir = os.path.join(project_util.RESULT_DIR, d,
                'pymsbayes-results')
        post_sample_path = os.path.join(result_dir, 'pymsbayes-output',
                'd1', 'm12345678-combined',
                'd1-m12345678-combined-s1-25-posterior-sample.txt.gz')
        scaled_post_path = os.path.join(result_dir,
                'rescaled-posterior.txt.gz')
        process_posterior(post_sample_path, scaled_post_path)

if __name__ == '__main__':
    main_cli()

