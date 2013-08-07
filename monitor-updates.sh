#!/bin/zsh
array=("${(@f)$(apt-get -s dist-upgrade | grep -P "\d+ upgraded, \d+ newly installed, \d+ to remove and \d+ not upgraded."| grep -oP "\d+")}")
echo "⬈ ${(j:/:)array} ·"
