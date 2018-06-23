__author__ = 'Suyash Soni'
__email__ = 'suyash.soni248@gmail.com'

import setuptools

setuptools.setup(
    name='sqlalchemy_json_querybuilder',
    version='1.1.4',
    author='Suyash Soni',
    author_email='suyash.soni248@gmail.com',
    description='Querybuilder to use SqlAlchemy ORM by feeding JSON/object as input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/suyash248/sqlalchemy-json-querybuilder',
    packages=['sqlalchemy_json_querybuilder'],
    python_requires='>=3',
    install_requires=[
		'SQLAlchemy'
	],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]

)