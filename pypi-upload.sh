#!/usr/bin/env bash

python3 setup.py sdist bdist_wheel
#rm -rf dist build sqlalchemy_json_querybuilder.egg-info
twine upload --repository-url https://test.pypi.org/legacy/ dist/*