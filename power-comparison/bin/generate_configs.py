#! /usr/bin/env python

import os
import sys
import math

import project_util
from project_util import SETTINGS

def write_observed_configs(output_dir):
    for upper_tau, cfg in SETTINGS.observed_cfg_iter():
        out_path = os.path.join(output_dir, 
                'observed-{0}.cfg'.format(upper_tau))
        with open(out_path, 'w') as out:
            out.write(cfg)

def write_exp_observed_configs(output_dir):
    for upper_tau, cfg in SETTINGS.observed_cfg_iter(uniform_tau=False):
        out_path = os.path.join(output_dir, 
                'exp-observed-{0}.cfg'.format(upper_tau))
        with open(out_path, 'w') as out:
            out.write(cfg)

def write_prior_configs(output_dir):
    for div_model, cfg in SETTINGS.prior_cfg_iter():
        out_path = os.path.join(output_dir, 
                'prior-{0}.cfg'.format(div_model))
        with open(out_path, 'w') as out:
            out.write(cfg)
    out_path = os.path.join(output_dir, 'prior-old.cfg')
    with open(out_path, 'w') as out:
        out.write(SETTINGS.get_old_prior())

def write_old_observed_configs(output_dir):
    for upper_tau, cfg in SETTINGS.old_observed_cfg_iter():
        out_path = os.path.join(output_dir, 
                'old-observed-{0}.cfg'.format(upper_tau))
        with open(out_path, 'w') as out:
            out.write(cfg)

def main():
    write_observed_configs(project_util.OBSERVED_CFG_DIR)
    write_exp_observed_configs(project_util.OBSERVED_CFG_DIR)
    write_old_observed_configs(project_util.OBSERVED_CFG_DIR)
    write_prior_configs(project_util.PRIOR_CFG_DIR)

if __name__ == '__main__':
    main()

