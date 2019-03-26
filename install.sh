#!/usr/bin/env bash

./build.sh
pip3 uninstall -y modular-conf
pip3 install --user dist/modular_conf-*.whl
