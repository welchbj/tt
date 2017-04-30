#!/bin/bash

set -e
set -x

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    case "${TT_PY_VER}" in
        py27)
            pyenv install 2.7.10
            pyenv virtualenv 2.7.10 tt-dev
            ;;

        py33)
            pyenv install 3.3.6
            pyenv virtualenv 3.3.6 tt-dev
            ;;

        py34)
            pyenv install 3.4.3
            pyenv virtualenv 3.4.3 tt-dev
            ;;

        py35)
            pyenv install 3.5.3
            pyenv virtualenv 3.5.3 tt-dev
            ;;

        py36)
            pyenv install 3.6.1
            pyenv virtualenv 3.6.1 tt-dev
            ;;
    esac

    pyenv rehash
    pyenv activate tt-dev
fi

which python
python -m pip install wheel
if [[ $RUN_FLAKE ]]; then python -m pip install flake8; fi
