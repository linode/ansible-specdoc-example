#!/bin/bash

for f in plugins/modules/*.py
do
  PYTHONWARNINGS="ignore" ansible-specdoc -i "$f" -jc; #> /dev/null || exit 1;
done