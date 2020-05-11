#!/bin/bash

set -ex

which python
python setup.py build
python setup.py develop
python ttasks.py test
if [[ $RUN_FLAKE ]]; then flake8 .; fi
