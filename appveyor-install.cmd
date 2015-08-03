"%sdkver%" -q -version:v7.0
call setenv /x64

rem install python packages
pip install --cache-dir c:/temp pyside
pip install --cache-dir c:/temp pygments
pip install --cache-dir c:/temp traits
pip install --cache-dir c:/temp traitsui
pip install --cache-dir c:/temp traits_enaml
pip install --cache-dir c:/temp enaml
pip install --cache-dir c:/temp coverage

rem install pyface
python setup.py develop
