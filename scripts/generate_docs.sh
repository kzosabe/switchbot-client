#!/bin/bash -eu
cd "$( dirname "$0" )"/..
poetry run sphinx-apidoc -f -o ./docs ./switchbot_client
poetry run sphinx-build ./docs ./docs/_build

