#!/bin/bash -eu
cd "$( dirname "$0" )"/..
poetry run tox --quiet
