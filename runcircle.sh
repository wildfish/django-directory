#!/bin/sh
coverage run --source="./directory" ./runtests.py
coverage html -d $CIRCLE_ARTIFACTS
