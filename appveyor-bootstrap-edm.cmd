@ECHO OFF		
SETLOCAL EnableDelayedExpansion		
		
rem Setup developing enviroment		
IF /I "%1" == "setup" GOTO setup		
		
:setup		
CALL powershell.exe -Command "(new-object net.webclient).DownloadFile('https://package-data.enthought.com/edm/win_x86_64/1.4/edm_1.4.0_x86_64.msi', 'edm.msi')"		
msiexec /qn /a edm.msi TARGETDIR=c:\		
GOTO end		
		
		
:end		
ENDLOCAL		
ECHO.Done
