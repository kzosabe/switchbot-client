#!/bin/bash -eu
cd "$( dirname "$0" )"/..
poetry run pytest -v --cov=switchbot_client --cov-report=html
