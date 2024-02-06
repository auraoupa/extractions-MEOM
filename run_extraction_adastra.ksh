#!/bin/bash

dataset=$1

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

python launch_dataset_extraction.py -dataset "${dataset%.*}"
python check_dataset_extraction.py -dataset "${dataset%.*}"
python save_dataset_extraction.py -dataset "${dataset%.*}"
