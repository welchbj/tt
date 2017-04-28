#!/bin/bash

if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
python -m pip install wheel

if [[ $TT_32_BIT ]]; then
    sudo apt-get install g++-multilib
    CFLAGS=-m32 LDFLAGS=-m32 python setup.py develop
else
    python setup.py develop
fi
