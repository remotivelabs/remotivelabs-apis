#!/bin/sh
mkdir -p doc/
pdoc \
    --favicon https://releases.remotivelabs.com/favicon.ico \
    --logo https://releases.remotivelabs.com/remotive-labs-logo-neg.png \
    --no-show-source \
    -t misc/theme \
    -o doc/ \
    ./remotivelabs
    # -np 3452

