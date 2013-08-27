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

staging_dir=$(mktemp -d /tmp/output.XXXXXXXXX)

reps=50000
nprocs=4
nprior=1000000
batch_size=25000
nsums=100000
npost=1000
nquantiles=1000
seed=37851841

output_dir="../results/no-sort"
if [ ! -d "$output_dir" ]
then
    mkdir -p $output_dir
fi

dmc.py --np $nprocs \
    -r $reps \
    -o ../configs/prior-dpp.cfg \
    -p ../no-sort/priors/pymsbayes-results/pymsbayes-output/prior-stats-summaries \
    -n $nprior \
    --prior-batch-size $batch_size \
    --num-posterior-samples $npost \
    --num-standardizing-samples $nsums \
    -q $nquantiles \
    --sort-index 0 \
    --output-dir $output_dir \
    --temp-dir $staging_dir \
    --staging-dir $staging_dir \
    --seed $seed \
    --no-global-estimate \
    --compress

echo "Here are the contents of the local temp directory '${staging_dir}':"
ls -Fla $staging_dir
echo 'Removing the local temp directory...'
rm -r $staging_dir
echo 'Done!'

