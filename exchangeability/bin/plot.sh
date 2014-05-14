#! /bin/bash

cfg_dir="../configs"
plot_dir="../plots"
nproc=8
if [ ! -d "$plot_dir" ]
then
    mkdir -p $plot_dir
fi

for config in ${cfg_dir}/*.cfg
do
    conf="$(basename $config)"
    prefix=${conf/\.cfg/}
    out_dir=${plot_dir}/${prefix}
    if [ ! -d "$out_dir" ]
    then
        mkdir $out_dir
    fi
    dmc_plot_stats.py -c "$config" -n 1000 --np $nproc --compress -o "$out_dir" --seed 199065646
done

