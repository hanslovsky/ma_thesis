#!/bin/bash

fns=$(ls t=*label.png -1 | sed 's/_label.png//g')
for f in $fns; do
    fraw="$f""_raw.png"
    flabel="$f""_label.png"
    ffit="$f""_fit.png"
    ncluster="${f: -1}"
    echo $fraw
    ./fit.py -a0.7 -l10 --raw "$fraw" -s"$flabel" -n"$ncluster" -o"$ffit"
done
