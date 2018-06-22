#!/usr/bin/env bash

rm -rf dist build sqlalchemy_json_querybuilder.egg-info
python3 setup.py sdist bdist_wheel

# For test.pypi
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# For pypi
twine upload dist/*