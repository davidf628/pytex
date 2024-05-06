#! /bin/bash

i=1;
s="";
for arg in "$@" 
do
    if [[ $arg = -* ]]
    then
        s="$s $arg"
    else
        s="$s \"$arg\""
    fi
    i=$((i + 1));
done

SOURCEFILE="/path/to/pytex.py"

if [ -f $SOURCEFILE ]; then
    python3 $SOURCEFILE $s
else
    echo "Cannot find pytex.py"
fi