#! /usr/bin/env python

import os
import sys
import math

BIN_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.dirname(BIN_DIR))
CONFIG_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'configs'))
RESULT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'results'))
OBSERVED_CFG_DIR = os.path.abspath(os.path.join(CONFIG_DIR, 'observed'))
PRIOR_CFG_DIR = os.path.abspath(os.path.join(CONFIG_DIR, 'prior'))
IMAGE_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'images'))

def get_exp_with_same_variance(uniform_max):
    uni_variance = (1/float(12)) * (float(uniform_max)**2)
    exp_mean = math.sqrt(uni_variance)
    return exp_mean

class SimulationSettings(object):
    def __init__(self, **kwargs):
        self.observed_upper_taus = list(kwargs.get('observed_upper_taus',
                [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0]))
        self.upper_tau = float(kwargs.get('upper_tau', 10.0))
        self.lower_theta = 0.0
        self.upper_theta = float(kwargs.get('upper_theta', 0.05))
        self.theta_scale = self.upper_theta / 2
        self.dpp_shape = float(kwargs.get('dpp_shape', 1.5))
        self.dpp_scale = float(kwargs.get('dpp_scale', (9.049851/0.5)))
        # with the concentration paramter, a = 9.049851, the function 
        #       p(k | a,n=22)
        # is maximized for k=11 and k=12. This setting places a 
        # gamma(1.5, (9.049851/0.5)) hyper-prior on `a` that has a mode of
        # 9.049851.

    def observed_cfg_iter(self, uniform_tau = True):
        for t in self.observed_upper_taus:
            yield t, '{0}\n{1}\n'.format(
                    self.get_observed_cfg_header(t, uniform_tau),
                    self.get_sample_table())

    def prior_cfg_iter(self, uniform_tau = False):
        for k, f in [('dpp', self.get_dpp_cfg_header), 
                ('uniform', self.get_uniform_cfg_header),
                ('u-shaped', self.get_u_shaped_cfg_header)]:
            yield k, '{0}\n{1}\n'.format(
                    f(self.upper_tau, psi = 0, uniform_tau = uniform_tau),
                    self.get_sample_table())

    def old_observed_cfg_iter(self, psi = 22):
        for t in self.observed_upper_taus:
            yield t, '{0}\n{1}\n'.format(
                    self.get_old_cfg_header(t, psi),
                    self.get_sample_table())

    def get_old_prior(self, psi = 0):
        return '{0}\n{1}\n'.format(
                    self.get_old_cfg_header(self.upper_tau, psi),
                    self.get_sample_table())

    def get_tau_settings(self, upper_tau, uniform_tau = True):
        if uniform_tau:
            return 0.0, -upper_tau
        else:
            return 1.0, get_exp_with_same_variance(upper_tau)

    def get_dpp_cfg_header(self, upper_tau, psi = 0, uniform_tau = True):
        return self.get_cfg_header(dpp_shape = self.dpp_shape,
                dpp_scale = self.dpp_scale,
                upper_tau = upper_tau,
                psi = psi,
                uniform_tau = uniform_tau)

    def get_uniform_cfg_header(self, upper_tau, psi = 0, uniform_tau = True):
        return self.get_cfg_header(dpp_shape = 0.0,
                dpp_scale = 0.0,
                upper_tau = upper_tau,
                psi = psi,
                uniform_tau = uniform_tau)

    def get_u_shaped_cfg_header(self, upper_tau, psi = 0, uniform_tau = True):
        return self.get_cfg_header(dpp_shape = -1.0,
                dpp_scale = -1.0,
                upper_tau = upper_tau,
                psi = psi,
                uniform_tau = uniform_tau)

    def get_observed_cfg_header(self, upper_tau, uniform_tau = True):
        return self.get_uniform_cfg_header(upper_tau = upper_tau,
                psi = 22,
                uniform_tau = uniform_tau)

    def get_cfg_header(self, dpp_shape, dpp_scale, upper_tau, psi = 0,
            uniform_tau = True):
        tau_shape, tau_scale = self.get_tau_settings(upper_tau,
                uniform_tau = uniform_tau)
        return """concentrationShape = {0}
concentrationScale = {1}
thetaShape = 1.0
thetaScale = {2}
ancestralThetaShape = 0
ancestralThetaScale = 0
thetaParameters = 012
tauShape = {3}
tauScale = {4}
bottleProportionShapeA = 1.0
bottleProportionShapeB = 1.0
bottleProportionShared = 0
numTauClasses = {5}
constrain = 0
subParamConstrain = 111111111
""".format(dpp_shape, dpp_scale, self.theta_scale, tau_shape, tau_scale, psi)

    def get_old_cfg_header(self, upper_tau, psi = 0):
        return """lowerTheta = 0.0
upperTheta = {0}
upperTau = {1}
numTauClasses = {2}
upperMig = 0.0
upperRec = 0.0
upperAncPopSize = 1.0
constrain = 0
subParamConstrain = 111111111
""".format(self.upper_theta, upper_tau, psi)

    def get_sample_table(self):
        return """BEGIN SAMPLE_TBL
Crocidura.beatus.Leyte_Samar	mt	1	1	12	11	25.53525	2032	0.31418	0.25732	0.11597	../sequences/Crocidura.beatus.Leyte_Samar.fasta
Crocidura.negrina-panayensis.Negros_Panay	mt	1	1	12	6	25.53525	2037	0.31418	0.25732	0.11597	../sequences/Crocidura.negrina-panayensis.Negros_Panay.fasta
Cynopterus.brachyotis.Biliran_Mindanao	mt	1	1	8	20	32.73678	600	0.37162	0.27929	0.12469	../sequences/Cynopterus.brachyotis.Biliran_Mindanao.fasta
Cynopterus.brachyotis.Negros_Panay	mt	1	1	8	14	32.73678	600	0.37162	0.27929	0.12469	../sequences/Cynopterus.brachyotis.Negros_Panay.fasta
Cyrtodactylus.gubaot-sumuroi.Leyte_Samar	mt	1	1	29	6	10.36282	1417	0.32164	0.27709	0.18956	../sequences/Cyrtodactylus.gubaot-sumuroi.Leyte_Samar.fasta
Cyrtodactylus.annulatus.Bohol_Mindanao	mt	1	1	3	14	10.36282	1420	0.32164	0.27709	0.18956	../sequences/Cyrtodactylus.annulatus.Bohol_Mindanao.fasta
Cyrtodactylus.philippinicus.Negros_Panay	mt	1	1	6	14	10.36282	1413	0.32164	0.27709	0.18956	../sequences/Cyrtodactylus.philippinicus.Negros_Panay.fasta
Dendrolaphis.marenae.Negros_Panay	mt	1	1	6	6	8.33769	1063	0.3284	0.26557	0.11906	../sequences/Dendrolaphis.marenae.Negros_Panay.fasta
Gekko.mindorensis.Negros_Panay	mt	1	1	8	11	8.48447	1297	0.33395	0.28914	0.12237	../sequences/Gekko.mindorensis.Negros_Panay.fasta
Haplonycteris.fischeri.Biliran_Mindanao	mt	1	1	8	29	22.51552	564	0.39836	0.2682	0.11952	../sequences/Haplonycteris.fischeri.Biliran_Mindanao.fasta
Haplonycteris.fischeri.Negros_Panay	mt	1	1	9	21	22.51552	564	0.39836	0.2682	0.11952	../sequences/Haplonycteris.fischeri.Negros_Panay.fasta
Hipposideros.obscurus.Leyte_Mindanao	mt	1	1	9	19	7.89455	1040	0.35217	0.30844	0.10147	../sequences/Hipposideros.obscurus.Leyte_Mindanao.fasta
Hipposideros.pygmaeus.Bohol_Mindanao	mt	1	1	12	3	7.89455	1044	0.35217	0.30844	0.10147	../sequences/Hipposideros.pygmaeus.Bohol_Mindanao.fasta
Limnonectes.leytensis.Bohol_Mindanao	mt	1	1	2	4	7.75057	2361	0.33977	0.23031	0.16702	../sequences/Limnonectes.leytensis.Bohol_Mindanao.fasta
Limnonectes.magnus.Bohol_Mindanao	mt	1	1	3	2	7.75057	2400	0.33977	0.23031	0.16702	../sequences/Limnonectes.magnus.Bohol_Mindanao.fasta
Macroglossus.minimus.Biliran_Mindanao	mt	1	1	4	19	26.53006	576	0.38173	0.25621	0.08506	../sequences/Macroglossus.minimus.Biliran_Mindanao.fasta
Macroglossus.minimus.Negros_Panay	mt	1	1	8	10	26.53006	576	0.38173	0.25621	0.08506	../sequences/Macroglossus.minimus.Negros_Panay.fasta
Ptenochirus.jagori.Leyte_Mindanao	mt	1	1	7	4	13.27737	681	0.38049	0.29526	0.08534	../sequences/Ptenochirus.jagori.Leyte_Mindanao.fasta
Ptenochirus.jagori.Negros_Panay	mt	1	1	8	8	13.27737	681	0.38049	0.29526	0.08534	../sequences/Ptenochirus.jagori.Negros_Panay.fasta
Ptenochirus.minor.Biliran_Mindanao	mt	1	1	9	30	13.27737	681	0.38049	0.29526	0.08534	../sequences/Ptenochirus.minor.Biliran_Mindanao.fasta
Insulasaurus.arborens.Negros_Panay	mt	1	1	22	10	4.78886	763	0.35955	0.30194	0.12976	../sequences/Insulasaurus.arborens.Negros_Panay.fasta
Pinoyscincus.jagori.Mindanao_Samar	mt	1	1	8	8	4.78886	756	0.35955	0.30194	0.12976	../sequences/Pinoyscincus.jagori.Mindanao_Samar.fasta

END SAMPLE_TBL
"""

SETTINGS = SimulationSettings()

def main():
    sys.stdout.write("%s" % PROJECT_DIR)

if __name__ == '__main__':
    main()

