#! /usr/bin/env python

import os
import sys

from pymsbayes.workers import EuRejectWorker, ABCToolBoxRegressWorker
from pymsbayes.utils.tempfs import TempFileSystem
import project_util


def get_regression_worker(temp_fs, posterior_path, observed_path):
    w = ABCToolBoxRegressWorker(
            temp_fs = temp_fs,
            observed_path = observed_path,
            posterior_path = posterior_path,
            num_posterior_quantiles = 10000,
            compress = True)
    return w
    
def get_reject_worker(temp_fs, prior_paths, observed_path, summary_path,
        out_dir):
    post_path = os.path.join(out_dir, 'posterior-sample.txt')
    reg_worker = get_regression_worker(temp_fs, post_path, observed_path,)
    w = EuRejectWorker(
            temp_fs = temp_fs,
            observed_path = observed_path,
            prior_paths = prior_paths,
            num_posterior_samples = 10000,
            summary_in_path = summary_path,
            posterior_path = post_path,
            regression_worker = reg_worker)
    return w


    
def main_cli():
    result_dir = os.path.join(project_util.PROJECT_DIR,
            'hickerson-et-al-posterior')
    assert os.path.isdir(result_dir)
    per_model_post_path = os.path.join(result_dir, 'per-model-posteriors.txt')
    assert os.path.isfile(per_model_post_path)
    observed_path = os.path.join(project_util.RESULT_DIR, 'sampling-error',
            'pymsbayes-results', 'observed-summary-stats', 'observed-1.txt')
    assert os.path.isfile(observed_path)
    summary_path = os.path.join(project_util.RESULT_DIR, 'hickerson',
            'pymsbayes-results', 'pymsbayes-output', 'prior-stats-summaries',
            'm12345678-combined-stat-means-and-std-devs.txt')
    assert os.path.isfile(summary_path)

    eureject_dir = os.path.join(result_dir, 'eureject-results')
    if not os.path.exists(eureject_dir):
        os.mkdir(eureject_dir)

    temp_fs = TempFileSystem(parent = eureject_dir)

    w = get_reject_worker(
            temp_fs = temp_fs,
            prior_paths = [per_model_post_path],
            observed_path = observed_path,
            summary_path = summary_path,
            out_dir = eureject_dir)
    w.start()


if __name__ == '__main__':
    main_cli()

