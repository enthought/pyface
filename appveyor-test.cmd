edm run -- invoke test --runtime=%python% --toolkit=%toolkit%
if %errorlevel% neq 0 exit /b %errorlevel%
coverage report --omit=*wx*
