@echo off
rem # This is the equivalent of a Makefile in Windows.
rem # This should be functionally equivalent to the Makefile found in the 
rem # same directory.

set TAG=[tt]
set REQS=%CD%\reqs
set DEVREQS=%REQS%\requirements-dev.txt
set TT_PYPI_NAME=ttable

if /I "%~1"=="" call :_help & exit /b
if /I "%~1"=="help" call :_help & exit /b
if /I "%~1"=="clean" call :clean & exit /b
if /I "%~1"=="test" call :test & exit /b
if /I "%~1"=="doc" call :doc & exit /b
if /I "%~1"=="flake8" call :flake8 & exit /b
if /I "%~1"=="upload" call :upload & exit /b
if /I "%~1"=="install-tt" call :install-tt & exit /b
if /I "%~1"=="install-reqs" call :install-reqs & exit /b
if /I "%~1"=="uninstall-tt" call :uninstall-tt & exit /b
if /I "%~1"=="uninstall-all" call :uninstall-all & exit /b
if /I "%~1"=="test-sdist" call :test-sdist & exit /b
if /I "%~1"=="test-bdist-wheel" call :test-bdist-wheel & exit /b
if /I "%~1"=="get-reqs" call :get-reqs & exit /b
if /I "%~1"=="update-reqs" call :write-reqs & exit /b
if /I "%~1"=="check-dev-env" call :check-dev-env & exit /b
if /I "%~1"=="check-all" call :check-all & exit /b
@echo Unknown target called. & exit /b 1

rem # === Standalone Targets =================================================

:_help
@echo TODO
exit /b

:clean
@echo TODO
exit /b

:test
@echo.
@echo %TAG% Running unit tests
@echo.
python -m unittest discover -s tt\tests\unit
@echo.
@echo.
@echo %TAG% Running functional tests
@echo.
python -m unittest discover -s tt\tests\functional
@echo.
exit /b

:doc
@echo TODO
exit /b

:flake8
@echo.
@echo %TAG% Running flake8...
flake8 --exclude=docs .
@echo %TAG% OK.
@echo.
exit /b

:install-tt
@echo.
@echo %TAG% Installing tt...
pip install --upgrade --editable . >nul 2>&1
where tt || @echo Installation of tt failed & exit /b 1
@echo %TAG% OK.
@echo.
exit /b

:install-reqs
@echo.
@echo %TAG% Installing dev requirements from %DEVREQS%...
pip install --upgrade -r %DEVREQS% >nul 2>&1
@echo %TAG% OK.
@echo.
exit /b

:uninstall-tt
@echo.
@echo %TAG% Uninstalling tt...
where tt >nul 2>&1 || @echo Cancelled uninstall; tt is already not installed. & exit /b 0
pip uninstall --yes %TT_PYPI_NAME% >nul 2>&1
where tt >nul 1 2>&1 && @echo Failed uninstall. & exit /b 1
@echo %TAG% OK.
@echo.
exit /b

:uninstall-reqs
@echo.
@echo %TAG% Uninstalling all tt dev requirements...
pip uninstall --yes -r %DEVREQS% >nul 2>&1
@echo %TAG% OK.
@echo.
exit /b

:update-reqs
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
python --version | findstr 3.* >nul 2>&1 || (@echo Python 3 is not active. & exit /b 1)
@echo %TAG% OK.
@echo.
@echo %TAG% Asserting a virtualenv is active...
python -c "import sys; print(hasattr(sys, 'real_prefix'))" | findstr /I true >nul 2>&1 || (@echo Not running inside virtualenv. & exit /b 1)
@echo %TAG% OK.
exit /b

rem # === Dependent Targets ==================================================

:upload
@echo TODO
exit /b

:init
@echo.
@echo %TAG% Beginning initialization of tt for testing...
call :clean
call :uninstall-reqs
call :uninstall-tt
call :install-reqs
call :install-tt
exit /b

:test-sdist
@echo TODO
exit /b

:test-bdist-wheel
@echo TODO
exit /b

:test-dist
@echo.
@echo %TAG% Testing source and binary distributions of tt...
call :test-sdist
call :test-bdist-wheel
exit /b

:check-all
@echo TODO
exit /b
