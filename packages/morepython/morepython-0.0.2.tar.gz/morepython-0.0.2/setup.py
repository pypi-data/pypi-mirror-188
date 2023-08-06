#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages


# Get metadata without importing the package
with open('morepython/metadata.py') as metadata_file:
    exec(metadata_file.read())
    metadata = locals()

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = []

setup(
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url=metadata['__url__'],
    version=metadata['__version__'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    description=metadata['__summary__'],
    install_requires=requirements,
    extras_require={
        'dev': [
            'flake8',
            'twine',
            'wheel',

            # Testing and coverage
            'pytest',
        ]
    },
    license='MIT license',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='utility',
    name='morepython',
    packages=find_packages(include=['morepython', 'morepython.*']),
    test_suite='tests',
)
