#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew install openssl readline xz python python3
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv

    pyenv install $TT_PY_VER
    export PYENV_VERSION=$TT_PY_VER
    export PATH="$HOME/.pyenv/shims:${PATH}"

    pyenv-virtualenv venv
    source venv/bin/activate

    python --version
fi

if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
python -m pip install wheel
python setup.py develop
