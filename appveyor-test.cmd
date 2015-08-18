mkdir testrun
copy .coveragerc testrun/
cd testrun
if %errorlevel% neq 0 exit /b %errorlevel%
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
