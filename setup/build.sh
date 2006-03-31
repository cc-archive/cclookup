#!/bin/sh

# Builds Win32 MSI for Creative Commons Tools
# copyright 2004, Creative Commons, Nathan R. Yergler
#
# usage:
# ./build.sh xxxxx
# where xxxxx is the new version number

export VERSION=$1
export PRODGUID=`uuidgen`

./_build.bat $VERSION $PRODGUID $PRODGUID
#./bin/candle build.wxs
#./bin/light build.wixobj

