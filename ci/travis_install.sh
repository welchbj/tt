#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    if [[ ${PYENV_VERSION:0:1} == "3" ]]; then
        # we need the Python dev headers
        brew install python3
    fi

    export PYENV_VERSION_STRING="Python ${PYENV_VERSION}"
    wget https://github.com/praekeltfoundation/travis-pyenv/releases/download/0.3.0/setup-pyenv.sh
    source setup-pyenv.sh
fi

if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
python -m pip install wheel
python setup.py develop
