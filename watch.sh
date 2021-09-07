#!/bin/sh

# No set -e as that breaks wait when there is an error.
# set -e

./build.sh $1;

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    -inotifywait -m -e close_write,moved_to --format %f . | \
    while read -r filename; \
        do if [ "$filename" = "$1" ]; then \
            ./build.sh $1; \
        fi; \
    done \
elif [[ "$OSTYPE" == "darwin"* ]]; then

    fswatch -o $1 | xargs -n1 -I{} ./build.sh $1;
fi

