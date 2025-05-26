#!/usr/bin/env bash
set -e
#config=/data/data_from_john/jax/jax_214_all_ba_including_config/config.json
#config=/data/data_from_john/jax/jax_068_crop_ba_rgb_part/config.json

if [ -n "$1" ]; then
    config="$1"
else
    config=/data/data_from_john/jax/jax_068_crop_ba_rgb_part/config.json
fi

s2p $config
