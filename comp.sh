#!/bin/bash

rm out/out*
python build.py 1234 hello
cd out
lilypond out.ly
open out.pdf