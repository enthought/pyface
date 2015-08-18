mkdir testrun
copy .coveragerc testrun/
cd testrun
if %errorlevel% neq 0 exit /b %errorlevel%
coverage run -m nose.core pyface -v --exclude='wx'
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
