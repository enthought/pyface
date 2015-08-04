if %ETS_TOOLKIT%==qt4 (
   coverage run -m nose.core -v --exclude-dir=pyface/ui/wx
) else (
   coverage run -m nose.core -v --exclude-dir=pyface/ui/qt
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report
