"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

rem install python packages
edm run -- invoke install --runtime=%python% --toolkit=%toolkit%
