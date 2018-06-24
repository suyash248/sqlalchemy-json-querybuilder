#!/usr/bin/env bash

rm -rf dist build sqlalchemy_json_querybuilder.egg-info

PY_REPO_URL=''
PYPI_USERNAME=''
IS_DIST=0
IS_UPLOAD=0
UPLOAD_DEST='pypi.org'

# Parsing cmd-args
while (( "$#" )); do
  case "$1" in
    -t|--test)
      UPLOAD_DEST='test.pypi.org'
      PY_REPO_URL='--repository-url https://test.pypi.org/legacy/ dist/*'
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
      echo "Usage:"
      echo "gunicorn.sh --host <hostname> --port <port> --virtualenv <virtual-env-name> --mode <mode> --workers <num> --daemon"
      exit 1
      ;;
    *) # preserve positional arguments
      shift
      ;;
  esac
done

if [[ "$IS_DIST" == 1 ]]
then
    echo "Creating dist..."
    python3 setup.py sdist bdist_wheel
fi

if [[ "$IS_UPLOAD" == 1 ]]
then
    echo "Uploading to $UPLOAD_DEST"
    twine upload $PY_REPO_URL dist/* -u $PYPI_USERNAME
fi