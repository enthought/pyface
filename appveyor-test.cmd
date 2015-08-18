mkdir testrun
copy .coveragerc testrun/
cd testrun
if %errorlevel% neq 0 exit /b %errorlevel%
IF %PYTHON% EQU "C:/Python27-x64" coverage run -m nose.core -v ../ --exclude-dir=../pyface/ui/wx
IF %PYTHON% EQU "C:/Python34-x64" coverage run -m nose.core -v ../ --exclude-dir=../pyface/ui/wx --exclude="enaml"

if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
