#!/usr/bin/env bash

rm -rf lib/*.egg-info/
rm -rf dist build sqlalchemy_json_querybuilder.egg-info

PY_REPO='pypi'
PYPI_USERNAME=''
IS_DIST=0
IS_UPLOAD=0

# Parsing cmd-args
while (( "$#" )); do
  case "$1" in
    -t|--test)
      PY_REPO='test.pypi'
      shift 1
      ;;
    -d|--dist)
      IS_DIST=1
      shift 1
      ;;
    --upload)
      IS_UPLOAD=1
      shift 1
      ;;
    -u|--username)
      PYPI_USERNAME=$2
      shift 2
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      shift
      ;;
  esac
done

export PY_REPO="$PY_REPO"

if [[ "$IS_DIST" == 1 ]]
then
    echo "[SETUP] Creating dist..."
    python3 setup.py sdist bdist_wheel
fi

if [[ "$IS_UPLOAD" == 1 ]]
then
    echo "[SETUP] Uploading to $PY_REPO"
    if [[ "$PY_REPO" == 'pypi' ]]
    then
        twine upload dist/* -u $PYPI_USERNAME
    else
        twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u $PYPI_USERNAME
    fi
fi

rm -rf lib/*.egg-info/
rm -rf dist build sqlalchemy_json_querybuilder.egg-info