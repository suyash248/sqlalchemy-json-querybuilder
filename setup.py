__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import setuptools
import requests

readme_url = 'https://raw.githubusercontent.com/suyash248/sqlalchemy-json-querybuilder/master/README.md'
long_description = requests.get(readme_url).text

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="sqlalchemy_json_querybuilder",
    version="1.1.4",
    author="Suyash Soni",
    author_email="suyash.soni248@gmail.com",
    description="Querybuilder to use SqlAlchemy ORM by feeding JSON/object as input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suyash248/sqlalchemy-json-querybuilder",
    packages=setuptools.find_packages(exclude=["examples", "README.md", "setup.py"]),
    python_requires='>=3',
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)