@echo off
rem # This is the equivalent of a Makefile in Windows.
rem # This should be functionally equivalent to the Makefile found in the 
rem # same directory.

set TAG=[tt]
set REQS=%CD%\reqs
set DEVREQS="%REQS%\requirements-dev.txt"
set TT_PYPI_NAME=ttable

if /I "%~1"=="" @echo You must specify a target. & exit /b
if /I "%~1"=="help" call :_help & exit /b
if /I "%~1"=="clean" call :clean & exit /b
if /I "%~1"=="flake8" call :flake8 & exit /b
if /I "%~1"=="install-tt" call :install-tt & exit /b
if /I "%~1"=="install-reqs" call :install-reqs & exit /b
if /I "%~1"=="uninstall-tt" call :uninstall-tt & exit /b
if /I "%~1"=="uninstall-reqs" call :uninstall-reqs & exit /b
if /I "%~1"=="write-reqs" call :write-reqs & exit /b
if /I "%~1"=="check-dev-env" call :check-dev-env & exit /b
if /I "%~1"=="test-sdist" call :test-sdist & exit /b
if /I "%~1"=="test-bdist-wheel" call :test-bdist-wheel & exit /b
if /I "%~1"=="test-dist" call :test-dist & exit /b
if /I "%~1"=="test" call :test & exit /b
if /I "%~1"=="init" call :init & exit /b
if /I "%~1"=="test-all" call :test-all & exit /b
if /I "%~1"=="upload" call :upload & exit /b

@echo Unknown target called. & exit /b 1

rem # === Standalone Targets =================================================


:clean
@echo %TAG% Cleaning environment...
del /s /q *.pyc >nul 2>&1
rmdir /s /q .tox >nul 2>&1
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
rmdir /s /q %TT_PYPI_NAME%.egg-info >nul 2>&1
@echo %TAG% OK.
@echo.
exit /b

:flake8
@echo %TAG% Running flake8...
flake8 . || exit /b
@echo %TAG% OK.
@echo.
exit /b

:install-tt
@echo %TAG% Installing tt...
pip install --upgrade --editable . >nul 2>&1
where tt >nul 2>&1 || @echo %TAG% Installation of tt failed & exit /b 1
@echo %TAG% OK.
@echo.
exit /b

:install-reqs
@echo %TAG% Installing dev requirements from %DEVREQS%...
pip install --upgrade -r %DEVREQS% >nul 2>&1
@echo %TAG% OK.
@echo.
exit /b

:uninstall-tt
@echo %TAG% Uninstalling tt...
where tt >nul 2>&1 || @echo %TAG% Cancelled uninstall; tt is already not installed. & @echo. & exit /b 0
pip uninstall --yes %TT_PYPI_NAME% >nul 2>&1
where tt >nul 1 2>&1 && @echo %TAG% Failed uninstall. & @echo. & exit /b 1
@echo %TAG% OK.
@echo.
exit /b

:uninstall-reqs
@echo %TAG% Uninstalling all tt dev requirements...
pip uninstall --yes -r %DEVREQS% >nul 2>&1
@echo %TAG% OK.
@echo.
exit /b

:write-reqs
@echo %TAG% Updating %DEVREQS% with the current environment's installed packages
pip freeze > %DEVREQS%
@echo %TAG% OK.
@echo %TAG% New contents of %DEVREQS% are:
type %DEVREQS%
exit /b

:check-dev-env
rem # An initial check to make sure that the environment is good for testing/publishing purposes.
rem # Checks that Python 3 is being run and that a virtualenv is active.
@echo %TAG% Asserting Python 3 is the active Python...
python --version | findstr 3.* >nul 2>&1 || (@echo %TAG% Python 3 is not active. & exit /b 1)
@echo %TAG% OK.
@echo.
@echo %TAG% Asserting a virtualenv is active...
python -c "import sys; print(hasattr(sys, 'real_prefix'))" | findstr /I true >nul 2>&1 || (@echo %TAG% Not running inside virtualenv. & exit /b 1)
@echo %TAG% OK.
@echo.
exit /b

rem # === Dependent Targets ==================================================

:test
call :init
@echo %TAG% Running tests...
@echo.
python -m unittest || exit /b
exit /b

:init
@echo %TAG% Beginning initialization of tt for testing...
@echo.
call :uninstall-tt
call :install-reqs
call :install-tt
exit /b

:test-sdist
call :uninstall-reqs
call :uninstall-tt
call :clean
@echo %TAG% Beginning test of source distribution...
python setup.py sdist >nul 2>&1
for %%f in (dist\*.zip) do set SDIST=%%f
pip install --force-reinstall --upgrade %SDIST% >nul 2>&1
where tt >nul 2>&1 || (@echo tt did not install properly from source dist. & exit /b 1)
@echo %TAG% OK.
@echo.
exit /b

:test-bdist-wheel
call :uninstall-reqs
call :uninstall-tt
call :clean
@echo %TAG% Beginning test of binary wheel distribution...
python setup.py bdist_wheel >nul 2>&1
for %%f in (dist\*.whl) do set WHLDIST=%%f
pip install --force-reinstall --upgrade %WHLDIST% >nul 2>&1
where tt >nul 2>&1 || (@echo tt did not install properly from wheel dist. & exit /b 1)
@echo %TAG% OK.
@echo.
exit /b

:test-dist
call :test-sdist
call :test-bdist-wheel
exit /b

:test-all
call :flake8 || exit /b
call :test || exit /b
call :test-dist || exit /b
exit /b

:upload
call :check-dev-env || exit /b
call :test-all || (@echo Cancelling upload; tests failed. & exit /b 1)
@echo python setup.py register

python setup.py sdist --formats=zip
python setup.py sdist --formats=gztar
python setup.py bdist_wheel
python setup.py build --plat-name=win32 bdist_msi
python setup.py build --plat-name=win-amd64 bdist_msi

for %%f in (dist\*) do @echo python setup.py upload %%f
exit /b
