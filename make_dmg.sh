#!/bin/sh

SOURCE='./dist'
VOLUMENAME=ccLookup
DESTNAME=$VOLUMENAME-$1.dmg

hdiutil create -volname ccLookup -srcfolder $SOURCE $DESTNAME

