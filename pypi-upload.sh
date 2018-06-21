#!/usr/bin/env bash

cd sqlalchemy_json_querybuilder
rm -rf dist build sqlalchemy_json_querybuilder.egg-info
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*