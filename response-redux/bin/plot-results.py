#! /usr/bin/env python

import os
import sys

from pymsbayes import plotting
from pymsbayes.utils.parsing import spreadsheet_iter
from pymsbayes.utils.stats import get_freqs, freq_less_than, median, mode_list

import project_util
from rescale_posteriors import get_posterior_plot, summarize_results

def plot_posterior(post_path):
    model_indices = range(1, 9)
    scaled_indices = [5, 6]
    sp, xlim, ylim = get_posterior_plot(post_path, model_indices,
                scaled_indices)
    rect = [0, 0, 1, 1]
    sp.fig.tight_layout(pad = 0.25, rect = rect)
    sp.reset_plot()
    sp.savefig(os.path.join(os.path.dirname(post_path),
            'mean_by_dispersion.pdf'))

def main_cli():
    prior_prob_omega_less_than = 0.0887
    for d in ['hickerson', 'alt']:
        result_dir = os.path.join(project_util.RESULT_DIR, d,
                'pymsbayes-results')
        post_path = os.path.join(result_dir, 'pymsbayes-output',
                'd1', 'm12345678-combined',
                'd1-m12345678-combined-s1-25-posterior-sample.txt.gz')
        plot_posterior(post_path)
        summarize_results(post_path)

    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'hickerson-posterior-1k')
    post_path = os.path.join(result_dir, 'posterior-from-mike-1k.txt.gz')
    plot_posterior(post_path)
    summarize_results(post_path)

    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'hickerson-posterior-10k')
    post_path = os.path.join(result_dir, 'posterior-from-mike-10k.txt.gz')
    plot_posterior(post_path)
    summarize_results(post_path)

    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior', 'eureject-results')
    post_path = os.path.join(result_dir, 'posterior-sample.txt.gz')
    plot_posterior(post_path)
    summarize_results(post_path)


if __name__ == '__main__':
    main_cli()

