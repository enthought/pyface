#!/bin/bash

PYVER=$(python -c "import sys; print('{}.{}'.format(*sys.version_info))")
PYTHON_VER=$(echo $PYVER | tr -d '.')

case $QT_API in
    pyside)
        BINDING_VER=1.2.4
        FILENAME=$QT_API-$BINDING_VER-cp$PYTHON_VER-none-linux_x86_64.whl
        ;;
    pyqt)
        BINDING_VER=4.11.4
        FILENAME=$QT_API-$BINDING_VER-cp$PYTHON_VER.tar.gz
        ;;
    pyqt5)
        BINDING_VER=
        FILENAME=$QT_API-$BINDING_VER-cp$PYTHON_VER.tar.gz
        ;;
    *)
        echo "Unsupported binding: $QT_API"
        exit 1
        ;;
 esac


echo "Building: $FILENAME"

BUILD_PREFIX=$HOME/build-prefix
mkdir -p $BUILD_PREFIX
BINDIR=$BUILD_PREFIX/bin
export PATH=$BINDIR:$PATH
LIBDIR=$BUILD_PREFIX/lib
export LD_LIBRARY_PATH=$LIBDIR
INCDIR=$BUILD_PREFIX/include
export CFLAGS="-I$INCDIR -L$LIBDIR"
export CXXFLAGS="-I$INCDIR -L$LIBDIR"
SITEDIR=$BUILD_PREFIX/lib/python$PYVER/site-packages
export PYTHONPATH=$SITEDIR

set -xe

function build_pyside()
{
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
}

function build_sip()
{
    echo "Building sip"
    SIP_VERSION=4.18
    SIP_FILE=~/sip-$SIP_VERSION.tar.gz
    curl -L -o $SIP_FILE http://sourceforge.net/projects/pyqt/files/sip/sip-$SIP_VERSION/sip-$SIP_VERSION.tar.gz
    echo "78724bf2a79878201c3bc81a1d8248ea  $HOME/sip-$SIP_VERSION.tar.gz" | md5sum -c -
    tar xf $SIP_FILE
    pushd sip-*
    python configure.py -b $BUILD_PREFIX/bin -d $SITEDIR -e $INCDIR
    make -j2
    make install
    python -m site
    python -c "import sip; print sip"
    popd
}

function build_pyqt()
{
    build_sip
    echo "Building PyQt4"
    curl -L -o ~/pyqt-$BINDING_VER.tar.gz http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-$BINDING_VER/PyQt-x11-gpl-$BINDING_VER.tar.gz
    echo "2fe8265b2ae2fc593241c2c84d09d481  $HOME/pyqt-$BINDING_VER.tar.gz" | md5sum -c -
    tar xf ~/pyqt-$BINDING_VER.tar.gz
    pushd PyQt-*
    python configure-ng.py -c --confirm-license -b $BUILD_PREFIX/bin -d $SITEDIR --sip-incdir $INCDIR
    make -j2
    cd ..
    tar cf ~/.cache/$FILENAME PyQt-*
    popd
}

function build_pyqt5()
{
    echo "Building PyQt5: Not implemented"
    exit 1
}


# Build the bindings
if [ -f "${HOME}/.cache/$FILENAME" ]; then
    echo "Cache file found: ${HOME}/.cache/$FILENAME"
else
    build_$QT_API
fi


if [ "$QT_API" = "pyside" ]; then
    # Install pyside wheel
    python -m pip install "${HOME}/.cache/$FILENAME"
else
    # make install the compiled pyqt archive bundle
    mkdir temp
    pushd temp
    tar xf "${HOME}/.cache/$FILENAME"
    pushd */
    make install
    popd
fi
