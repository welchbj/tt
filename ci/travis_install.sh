#!/bin/bash

set -ex

which python
python -m pip install wheel
if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
