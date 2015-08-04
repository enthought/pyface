coverage run -m nose.core -v --exclude-dir=pyface/ui/wx
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
