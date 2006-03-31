#!/bin/bash

export cxpath=/opt/cx_Freeze-3.0
export APPNAME=lookup
export DISTDIR=$APPNAME-$1

mkdir $DISTDIR

$cxpath/FreezePython --install-dir=$DISTDIR ../lookup.py
cp ../*.xrc $DISTDIR
cp ../LICENSE $DISTDIR
cp ../README $DISTDIR

tar czvf $APPNAME-$1.tgz $DISTDIR

rm -rf $DISTDIR

