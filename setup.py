__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy_json_querybuilder",
    version="1.1.0",
    author="Suyash Soni",
    author_email="suyash.soni248@gmail.com",
    description="SqlAlchemy Querybuilder (JSON)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suyash248/sqlalchemy-json-querybuilder",
    packages=setuptools.find_packages(exclude=["examples", "README.md", "setup.py"]),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)