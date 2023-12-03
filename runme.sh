#!/bin/bash

DAY=$1
if [ -z "$1" ]; then
    echo "Usage: $0 <day> test?"
    exit 1
fi
DAY=$(printf "%02d" $1)
shift

find "__pycache__/Volumes" -type f -delete
python3 -X pycache_prefix=./__pycache__ src/2023/day-${DAY}.py "$@"