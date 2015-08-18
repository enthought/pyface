mkdir testrun
copy .coveragerc testrun/
cd testrun
if %errorlevel% neq 0 exit /b %errorlevel%
if %PYTHON% EQU "C:/Python27-x64" (
   coverage run -m nose.core -v ../ --exclude-dir=../pyface/ui/wx)
else (
   coverage run -m nose.core -v ../ --exclude-dir=../pyface/ui/wx --exclude="enaml")
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
