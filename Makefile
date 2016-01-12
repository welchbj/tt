TAG=[tt]
DEVREQS="./reqs/requirements-dev.txt"
TT_PYPI_NAME=ttable

all:
	@ echo

clean:
	@ echo $(TAG) Cleaning environment...
	@ find . -type f -name "*.py[co]" -delete
	@ find . -type d -name "__pycache__" -delete 
	@ rm -rf build 
	@ rm -rf dist 
	@ rm -rf $(TT_PYPI_NAME).egg-info
	@ echo $(TAG) OK.
	@ echo

py-version:
	@ echo ----------------------------
	@ echo Running with Python version:
	@ echo ----------------------------
	@ echo
	@ python --version
	@ echo
	@ echo ----------------------------
	@ echo
	@ echo
	@ echo

install-tt:
	@ echo $(TAG) Installing tt...
	@ pip install --upgrade --editable . >/dev/null
	@ which tt >/dev/null
	@ echo $(TAG) OK.
	@ echo

install-reqs:
	@ echo $(TAG) Installing dev requirements from $(DEVREQS)...
	@ pip install --upgrade -r $(DEVREQS) >/dev/null
	@ echo $(TAG) OK.
	@ echo

uninstall-tt:
	@ echo $(TAG) Uninstalling tt...
	@ pip uninstall --yes $(TT_PYPI_NAME) >/dev/null 2>&1 || echo $(TAG) tt is already not installed.
	@ ! which tt >/dev/null 2>&1
	@ echo $(TAG) OK.
	@ echo

uninstall-reqs:
	@ echo $(TAG) Uninstalling all tt dev requirements...
	@ pip uninstall --yes -r $(DEVREQS) >/dev/null 2>&1
	@ echo $(TAG) OK.
	@ echo

write-reqs:
	@ echo $(TAG) Updating $(DEVREQS) with the current environment\'s installed packages...
	@ pip freeze > $(DEVREQS)
	@ echo $(TAG) OK.
	@ echo $(TAG) New contents of $(DEVREQS) are:
	@ cat $(DEVREQS)
	@ echo

init: uninstall-tt install-reqs install-tt
	@ echo

test: init
	@ echo $(TAG) Running tests...
	@ python -m unittest discover -s tt
	@ echo

test-sdist: uninstall-tt uninstall-reqs clean
	@ echo $(TAG) Beginning test of source distribution...
	@ python setup.py sdist >/dev/null 2>&1
	@ pip install --force-reinstall --upgrade dist/* >/dev/null 2>&1
	@ which tt >/dev/null
	@ echo $(TAG) OK.
	@ echo

test-bdist-wheel: uninstall-tt uninstall-reqs clean
	@ echo $(TAG) Beginning test of binary wheel distribution...
	@ python setup.py bdist_wheel >/dev/null 2>&1
	@ pip install --force-reinstall --upgrade dist/* >/dev/null 2>&1
	@ which tt >/dev/null
	@ echo $(TAG) OK.
	@ echo

test-dist: test-sdist test-bdist-wheel
	@ echo

test-all: py-version test test-dist
	@ echo

upload: test-all
	@ python setup.py register

	@ python setup.py sdist --formats=zip
	@ python setup.py sdist --formats=gztar
	@ python setup.py bdist_wheel
	@ python setup.py build --plat-name=win32 bdist_msi
	@ python setup.py build --plat-name=win-amd64 bdist_msi

	@ python setup.py upload dist/*
