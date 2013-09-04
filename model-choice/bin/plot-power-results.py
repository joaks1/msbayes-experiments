#! /usr/bin/env python

import os
import sys

from pymsbayes.utils.parsing import DMCSimulationResults, spreadsheet_iter
from pymsbayes.config import MsBayesConfig
from pymsbayes.plotting import PsiPowerPlotGrid
from pymsbayes.utils.messaging import get_logger
import project_util

_LOG = get_logger(__name__)
POWER_INFO_PATH = os.path.join(project_util.RESULT_DIR, 'power',
        'pymsbayes-results', 'pymsbayes-info.txt')
RESULT_DIR = os.path.dirname(POWER_INFO_PATH)

class PowerResult(object):
    def __init__(self):
        self.true = []
        self.mode = []
        self.mode_glm = []
        self.median = []
        self.prob = []
        self.prob_glm = []

    @classmethod
    def parse_result_summary(cls, result_summary_path):
        psi = cls()
        omega = cls()
        for d in spreadsheet_iter([result_summary_path]):
            psi.true.append(int(d['psi_true']))
            psi.mode.append(int(d['psi_mode']))
            psi.mode_glm.append(int(round(float(d['psi_mode_glm']))))
            psi.prob.append(float(d['psi_1_prob']))
            psi.prob_glm.append(float(d['psi_1_prob_glm']))
            omega.true.append(float(d['omega_true']))
            omega.mode.append(float(d['omega_mode']))
            omega.median.append(float(d['omega_median']))
            omega.mode_glm.append(float(d['omega_mode_glm']))
            omega.prob.append(float(d['omega_prob_less']))
            omega.prob_glm.append(float(d['omega_prob_less_glm']))
        return psi, omega

def parse_results(info_path):
    dmc_sim = DMCSimulationResults(info_path)
    psi_results = {}
    omega_results = {}
    observed_configs = {}
    for k, v in dmc_sim.observed_index_to_config.iteritems():
        observed_configs[k] = MsBayesConfig(v)
    prior_index = '{0}-combined'.format(''.join(
            sorted([str(i) for i in dmc_sim.prior_index_to_config.iterkeys()])))
    for observed_index, cfg in observed_configs.iteritems():
        result_path = dmc_sim.get_result_summary_path(observed_index,
                prior_index)
        psi, omega = PowerResult.parse_result_summary(result_path)
        psi_results[cfg] = psi
        omega_results[cfg] = omega
    return psi_results, omega_results

def main_cli():
    psi_results, omega_results = parse_results(POWER_INFO_PATH)
    cfg_to_psi = {}
    for cfg, psi in psi_results.iteritems():
        cfg_to_psi[cfg] = psi.mode

    psi_plot = PsiPowerPlotGrid(observed_config_to_estimates = cfg_to_psi,
            num_taxon_pairs = 22,
            num_columns = 2)
    fig = psi_plot.create_grid()
    fig.savefig('psi_power.pdf')

if __name__ == '__main__':
    main_cli()

