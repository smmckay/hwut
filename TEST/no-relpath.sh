#! /usr/bin/env bash

if [ "$1" = "--hwut-info" ]; then
    echo "Misc: no module shall use 'os.path.relpath';"
    echo "HAPPY: [0-9]+;"
    exit
fi

echo 
echo "Make sure that modules do not use 'os.path.relpath'."
echo "This causes trouble under Windows with driver letters."
echo "They shall use 'hwut.auxiliary.path.relative(...)' instead."
echo 

pushd .. >& /tmp/null
grep -sHIne '\<relpath\>' . -r --include "*.py" 
popd >& /tmp/null

