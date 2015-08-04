"%sdkver%" -q -version:v7.0
call setenv /x64

rem install python packages
pip install --cache-dir c:/temp nose
pip install --cache-dir c:/temp nose-exclude
pip install --cache-dir c:/temp mock
if %ETS_TOOLKIT%==qt4 (
   pip install --cache-dir c:/temp pyside
) else (
   wxPython.exe /sp- /verysilent /norestart /SUPPRESSMSGBOXES)
pip install --cache-dir c:/temp pygments
pip install --cache-dir c:/temp traits
pip install --cache-dir c:/temp traitsui
pip install --cache-dir c:/temp traits_enaml
pip install --cache-dir c:/temp enaml
pip install --cache-dir c:/temp coverage

rem install pyface
python setup.py develop
