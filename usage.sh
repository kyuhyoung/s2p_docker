#!/usr/bin/env bash
set -e
#config=/data/data_from_john/jax/jax_214_all_ba_including_config/config.json
#config=/data/data_from_john/jax/jax_068_crop_ba_rgb_part/config.json

if [ -n "$1" ]; then
    config="$1"
else
    config=/data/data_from_john/jax/jax_068_crop_ba_rgb_part/config.json
    #config=/data/data_from_adel/gangnam_4_s2p/config.json
fi

if [ -n "$2" ]; then
    from_start="$2"
else
    from_start="0"
fi

if [ -n "$3" ]; then
    folder_plys="$3"
else
    folder_plys="/data/data_from_john/jax/jax_068_crop_ba_rgb_part/s2p_out/tiles"
    #folder_plys="/data/"
fi

if [ -n "$4" ]; then
    ply_merged="$4"
else
    ply_merged="/data/data_from_john/jax/jax_068_crop_ba_rgb_part/s2p_out/cloud.ply"
fi

s2p --start_from $from_start $config
python3 merge_ply.py --ply_folder $folder_plys --output_file $ply_merged
