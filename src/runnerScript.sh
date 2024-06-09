#!/bin/sh

filePath="$1"

echo $filePath

if [ ! -z "$filePath" ]; then
    # Extract extension from file path
    extension="${filePath##*.}"
    echo $extension
    if [ "$extension" = "bhau" ]; then
        echo "File has bhau extension"
    else
        echo "File does not have bhau extension"
        exit 1
    fi
else
    echo "No file provided"
    exit 1
fi


python3 ./runnerPyScript.py "$1"
