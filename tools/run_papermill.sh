#!/bin/bash

set -eux

# activate our virtualenv (this was created using pyenv-virtualenv, yours will be elsewhere)
source /Users/mcw/.pyenv/versions/3.8.6/envs/pandas/bin/activate 

# get to the script directory if running via cron
cd $(dirname "${BASH_SOURCE[0]}")

for S in AAPL MSFT GOOG FB
do
        papermill -p symbol $S papermill_example2.ipynb papermill_${S}.ipynb
        jupyter-nbconvert --no-input --to html papermill_${S}.ipynb
done

