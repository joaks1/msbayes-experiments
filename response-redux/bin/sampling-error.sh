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


nprocs=8
nprior=100000000
batch_size=12500
nsums=100000
npost=1000
nquantiles=1000
report_freq=5
seed=451864768

output_dir="../results/sampling-error"
if [ ! -d "$output_dir" ]
then
    mkdir -p $output_dir
fi

dmc.py --np $nprocs \
    -o ../configs/m6.cfg \
    -p ../configs/m6.cfg \
    -n $nprior \
    --prior-batch-size $batch_size \
    --num-posterior-samples $npost \
    --num-standardizing-samples $nsums \
    -q $nquantiles \
    --output-dir $output_dir \
    --staging-dir $staging_dir \
    --reporting-frequency $report_freq \
    --seed $seed

echo "Here are the contents of the local temp directory '${staging_dir}':"
ls -Fla $staging_dir
echo 'Removing the local temp directory...'
rm -r $staging_dir
echo 'Done!'

