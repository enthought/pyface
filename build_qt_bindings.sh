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
        BINDING_VER=5.5.1
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

SIP_VERSION=4.18
SIP_FILE=~/.cache/sip-$SIP_VERSION.tar.gz

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
    curl -L -o $SIP_FILE http://sourceforge.net/projects/pyqt/files/sip/sip-$SIP_VERSION/sip-$SIP_VERSION.tar.gz
    echo "78724bf2a79878201c3bc81a1d8248ea  $SIP_FILE" | md5sum -c -
    tar xf $SIP_FILE
    pushd sip-*
    python configure.py -b $BUILD_PREFIX/bin -d $SITEDIR -e $INCDIR
    make -j2
    make install
    cd ..
    tar cf $SIP_FILE sip-*
    python -m site
    python -c "import sip; print(sip)"
    popd
}

function build_pyqt()
{
    echo "Building PyQt4"
    curl -L -o ~/pyqt-$BINDING_VER.tar.gz http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-$BINDING_VER/PyQt-x11-gpl-$BINDING_VER.tar.gz
    echo "2fe8265b2ae2fc593241c2c84d09d481  $HOME/pyqt-$BINDING_VER.tar.gz" | md5sum -c -
    tar xf ~/pyqt-$BINDING_VER.tar.gz
    pushd PyQt-*
    python configure-ng.py -c --confirm-license -b $BUILD_PREFIX/bin -d $SITEDIR --sip-incdir $INCDIR --no-designer-plugin --no-sip-files
    make -j2
    cd ..
    tar cf ~/.cache/$FILENAME PyQt-*
    popd
}


function install_qt5()
{
    QTVER=5.6.0
    echo "Installing Qt $QTVER"
    curl -L -o ~/qt-opensource-linux-x64-$QTVER.run http://download.qt.io/official_releases/qt/5.6/$QTVER/qt-opensource-linux-x64-$QTVER.run
    echo "8ef8e13a8142b51987b4656e97e58c3a  $HOME/qt-opensource-linux-x64-$QTVER.run" | md5sum -c -
    chmod a+x ~/qt-opensource-linux-x64-$QTVER.run
    # Install into ~/Qt
    ~/qt-opensource-linux-x64-5.6.0.run --script qt-scripted-install.js --verbose
}

function build_pyqt5()
{
    echo "Building PyQt5"
    curl -L -o ~/pyqt-$BINDING_VER.tar.gz http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-$BINDING_VER/PyQt-gpl-$BINDING_VER.tar.gz
    echo "586ed481b734c665b52fbb4f32161ff7  $HOME/pyqt-$BINDING_VER.tar.gz" | md5sum -c -
    tar xf ~/pyqt-$BINDING_VER.tar.gz
    pushd PyQt-*
    python configure.py -c --confirm-license -b $BUILD_PREFIX/bin -d $SITEDIR --sip-incdir $INCDIR --qmake $HOME/Qt/5.6/gcc_64/bin/qmake --no-designer-plugin --no-sip-files
    make -j2
    cd ..
    tar cf ~/.cache/$FILENAME PyQt-*
    popd
}


if [ "$QT_API" = "pyside" ]; then
    # Install pyside wheel
    if [ -f "${HOME}/.cache/$FILENAME" ]; then
        echo "Cache file found: ${HOME}/.cache/$FILENAME"
    else
        build_$QT_API
    fi
    python -m pip install "${HOME}/.cache/$FILENAME"
else
    # Build pyqt bindings
    if [ "$QT_API" = "pyqt5" ]; then
        install_qt5
    fi
    build_sip
    build_$QT_API

    # Install the built tarball
    mkdir pyqt
    pushd pyqt
    tar xf "${HOME}/.cache/$FILENAME"
    pushd */
    make install
    popd
    popd
fi
