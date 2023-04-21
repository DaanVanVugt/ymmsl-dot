#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


# replace relative url with an URL to github
long_description = read("README.md").replace('./docs', 'https://github.com/DaanVanVugt/ymmsl-dot/raw/main/docs')

setup(
    name="ymmsl-dot",
    version="0.1.1",
    description="Visualise yMMSL models with graphviz.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    author="Daan van Vugt",
    author_email="dvanvugt@ignitioncomputing.com",
    url="https://github.com/DaanVanVugt/ymmsl-dot",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    project_urls={
        "webpage": "https://github.com/DaanVanVugt/ymmsl-dot",
        "Documentation": "https://ymmsl-dot.readthedocs.io/en/latest/",
        "Issue Tracker": "https://github.com/DaanVanVugt/ymmsl-dot/issues",
        "Discussion Forum": "https://github.com/DaanVanVugt/ymmsl-dot/discussions",
    },
    keywords=[
        "ymmsl",
        "simulation",
        "graphviz",
        "dot",
        "muscle3",
        "yMMSL",
        "multiscale",
    ],
    python_requires=">=3.7, <4",
    install_requires=[
        # https://stackoverflow.com/questions/14399534
        "pydot>=1",
        "ymmsl",
        "click",
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
    ],
    entry_points={
        "console_scripts": [
            "ymmsl = ymmsl_dot.main:main",
        ]
        #
    },
)
