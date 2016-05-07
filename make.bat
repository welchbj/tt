@ECHO off

REM # This should be functionally equivalent to the Makefile found in the
REM # same directory.

SET TAG=[tt]
SET REQS=%CD%\reqs
SET DEVREQS="%REQS%\requirements-dev.txt"
SET TT_PYPI_NAME=ttable

IF NOT "x%1"=="x" CALL :%1 || EXIT /B 1
EXIT /B 0

:clean
ECHO %TAG% Cleaning environment...
DEL /s /q *.pyc >nul 2>&1
RD /s /q build >nul 2>&1
RD /s /q dist >nul 2>&1
RD /s /q %TT_PYPI_NAME%.egg-info >nul 2>&1
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:py-version
ECHO ----------------------------
ECHO Running with Python version:
ECHO ----------------------------
ECHO.
python --version
ECHO.
ECHO ----------------------------
ECHO.
EXIT /B 0

:install-tt
ECHO %TAG% Installing tt...
pip install --upgrade --editable . >nul 2>&1
CALL where tt >nul 2>&1 || (ECHO %TAG% Installation of tt failed. & ECHO. & EXIT /b 1)
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:install-reqs
ECHO %TAG% Installing dev requirements from %DEVREQS%...
pip install --upgrade -r %DEVREQS% >nul 2>&1
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:uninstall-tt
ECHO %TAG% Uninstalling tt...
CALL where tt >nul 2>&1 || (ECHO %TAG% Cancelled uninstall; tt is already not installed. & ECHO. & EXIT /B 0)
pip uninstall --yes %TT_PYPI_NAME% >nul 2>&1
CALL where tt >nul 1 2>&1 && (ECHO %TAG% Failed uninstall. & ECHO. & EXIT /B 1)
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:uninstall-reqs
ECHO %TAG% Uninstalling all tt dev requirements...
pip uninstall --yes -r %DEVREQS% >nul 2>&1
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:write-reqs
ECHO %TAG% Updating %DEVREQS% with the current environment's installed packages
pip freeze > %DEVREQS%
ECHO %TAG% OK.
ECHO %TAG% New contents of %DEVREQS% are:
TYPE %DEVREQS%
EXIT /B 0

:init
ECHO %TAG% Beginning initialization of tt for testing...
ECHO.
CALL :uninstall-tt || EXIT /B 1
CALL :install-reqs || EXIT /B 1
CALL :install-tt || EXIT /B 1
EXIT /B 0

:test
CALL :init || EXIT /B 1
ECHO %TAG% Running tests...
ECHO.
CALL python -m unittest discover -s tt || EXIT /B 1
ECHO.
EXIT /B 0

:test-sdist
CALL :uninstall-reqs
CALL :uninstall-tt
CALL :clean
ECHO %TAG% Beginning test of source distribution...
python setup.py sdist >nul 2>&1
FOR %%f IN (dist\*.zip) DO SET SDIST=%%f
pip install --force-reinstall --upgrade %SDIST% >nul 2>&1
CALL where tt >nul 2>&1 || (ECHO %TAG% tt did not install properly from source dist. & EXIT /B 1)
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:test-bdist-wheel
CALL :uninstall-reqs || EXIT /B 1
CALL :uninstall-tt || EXIT /B 1
CALL :clean || EXIT /B 1
ECHO %TAG% Beginning test of binary wheel distribution...
python setup.py bdist_wheel >nul 2>&1
FOR %%f IN (dist\*.whl) DO SET WHLDIST=%%f
pip install --force-reinstall --upgrade %WHLDIST% >nul 2>&1
CALL where tt >nul 2>&1 || (ECHO %TAG% tt did not install properly from wheel dist. & EXIT /B 1)
ECHO %TAG% OK.
ECHO.
EXIT /B 0

:test-dist
CALL :test-sdist || EXIT /B 1
CALL :test-bdist-wheel || EXIT /B 1
EXIT /B 0

:test-all
CALL :py-version || EXIT /B 1
CALL :test || EXIT /B 1
CALL :test-dist || EXIT /B 1
EXIT /B 0

:upload
REM CALL :test-all || (ECHO Cancelling upload; tests failed. & EXIT /b 1)
REM python setup.py register
REM
python setup.py sdist --formats=zip
python setup.py sdist --formats=gztar
python setup.py bdist_wheel
python setup.py build --plat-name=win32 bdist_msi
python setup.py build --plat-name=win-amd64 bdist_msi

SETLOCAL EnableDelayedExpansion
SET ARTIFACTS=
FOR %%f IN (dist\*) DO SET ARTIFACTS=!ARTIFACTS! "%%f"
ECHO python setup.py !ARTIFACTS! upload
ENDLOCAL
EXIT /B 0
