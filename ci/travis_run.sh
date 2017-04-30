#!/bin/bash

set -e
set -x

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv activate tt-dev
fi

which python
python setup.py build
python setup.py develop
python ttasks.py test
if [[ $RUN_FLAKE ]]; then flake8 .; fi
