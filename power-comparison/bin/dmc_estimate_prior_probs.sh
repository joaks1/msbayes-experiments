#! /bin/sh
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -l h_vmem=16G
#$ -l vf=16G
#$ -q all.q
#$ -pe orte 8

if [ -n "$SGE_O_WORKDIR" ]
then
    source ~/.bash_profile
    cd /share/work1
    cd $SGE_O_WORKDIR
fi

nprocs=8
nprior=10000000
seed=53468713

dmc_estimate_prior_probs.py --np $nprocs \
    -n $nprior \
    --seed $seed \
    ../configs/prior/*.cfg > prior_prob_estimates.txt

