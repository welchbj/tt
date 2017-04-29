#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    export LDFLAGS="-Wl,-export_dynamic"
    export PYENV_VERSION_STRING="Python ${PYENV_VERSION}"
    wget https://github.com/praekeltfoundation/travis-pyenv/releases/download/0.3.0/setup-pyenv.sh
    source setup-pyenv.sh
fi

if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
python -m pip install wheel
python setup.py develop
