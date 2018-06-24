__author__ = 'Suyash Soni'
__email__ = 'suyash.soni248@gmail.com'

import os
from setuptools import setup, find_packages
from src.conf.settings import VERSION

def curr_version():
    py_repo = os.environ['PY_REPO']
    version = VERSION[py_repo]
    print('[SETUP] Preparing sqlalchemy_json_querybuilder-{version} to upload to {py_repo}'.format(
        version=version, py_repo=py_repo
    ))
    return version

setup(
    name='sqlalchemy_json_querybuilder',
    version=curr_version(),
    author='Suyash Soni',
    author_email='suyash.soni248@gmail.com',
    maintainer="Suyash Soni",
    description='Querybuilder to use SqlAlchemy ORM by feeding JSON/object as input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/suyash248/sqlalchemy-json-querybuilder',

    packages=find_packages('lib'),
    package_dir={
        '': 'lib'
    },

    python_requires='>=3',
    install_requires=[
		'sqlalchemy'
	],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

)