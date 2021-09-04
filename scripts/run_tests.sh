#!/bin/bash -eux
poetry run pylint switchbot_client
poetry run black switchbot_client tests --check --diff
poetry run pytest tests
