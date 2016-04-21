#!/bin/bash

PYTHON_VER=$(python -c "import sys; print('{}{}'.format(*sys.version_info))")

case $QT_API in
    pyside)
        BINDING_VER=1.2.4
        ;;
    pyqt)
        BINDING_VER=
        ;;
    pyqt5)
        BINDING_VER=
        ;;
    *)
        echo "Unsupported binding: $QT_API"
        exit 1
        ;;
 esac


FILENAME=$QT_API-$BINDING_VER-cp$PYTHON_VER-none-linux_x86_64.whl

echo "Building: $FILENAME"

set -xe

function build_pyside()
{
    if [ -f "${HOME}/.cache/$FILENAME" ]; then
        echo "PySide wheel found"
    else
        echo "Building PySide"
        git clone https://github.com/PySide/pyside-setup.git
        pushd pyside-setup

        # The normal pyside repos only have the right tags upto 1.1.1
        # So we need to replace the repos with the newer ones
        git submodule sync

        # now it is time to build the pyside wheels
        python setup.py bdist_wheel --qmake=/usr/bin/qmake-qt4 --version=$BINDING_VER --jobs=2
        ls dist/
        cp dist/PySide-$BINDING_VER-*.whl $HOME/.cache/$FILENAME
        popd
    fi
}

function build_pyqt()
{
    echo "Building PyQt4"
}

function build_pyqt5()
{
    echo "Building PyQt5"
}

# Build the bindings
build_$QT_API

python -m pip install "${HOME}/.cache/$FILENAME"
