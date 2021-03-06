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
    staging_dir=$(mktemp -d /tmp/output.XXXXXXXXX)
else
    staging_dir="../tmp"
    if [ ! -d "$staging_dir" ]
    then
        mkdir $staging_dir
    fi
fi

reps=1000
nprocs=8
nprior=2000000
batch_size=25000
nsums=100000
seed=44112330

output_dir="../priors"
if [ ! -d "$output_dir" ]
then
    mkdir -p $output_dir
fi

dmc.py --np $nprocs \
    -r 1 \
    -o ../configs/observed/*observed-0.2.cfg \
    -p ../configs/prior/prior-*.cfg \
    -n $nprior \
    --prior-batch-size $batch_size \
    --num-standardizing-samples $nsums \
    --sort-index 7 \
    --output-dir $output_dir \
    --staging-dir $staging_dir \
    --seed $seed \
    --generate-samples-only

echo "Here are the contents of the local temp directory '${staging_dir}':"
ls -Fla $staging_dir
echo 'Removing the local temp directory...'
rm -r $staging_dir
echo 'Done!'

