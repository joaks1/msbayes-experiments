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

nprocs=4
nprior=1000
batch_size=250
nsums=1000
seed=2617237416

output_dir="../priors-for-pc-plot"
if [ ! -d "$output_dir" ]
then
    mkdir -p $output_dir
fi

dmc.py --np $nprocs \
    -r 1 \
    -o ../configs/m1.cfg \
    -p ../configs/m1*.cfg ../configs/m[345].cfg\
    -n $nprior \
    --prior-batch-size $batch_size \
    --num-standardizing-samples $nsums \
    --sort-index 7 \
    --output-dir $output_dir \
    --staging-dir $staging_dir \
    --temp-dir $staging_dir \
    --seed $seed \
    --generate-samples-only

echo "Here are the contents of the local temp directory '${staging_dir}':"
ls -Fla $staging_dir
echo 'Removing the local temp directory...'
rm -r $staging_dir
echo 'Done!'

