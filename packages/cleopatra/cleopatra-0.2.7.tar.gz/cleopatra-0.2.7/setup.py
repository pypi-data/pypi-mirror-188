# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleopatra']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'serapeum_utils>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'cleopatra',
    'version': '0.2.7',
    'description': 'visualization package',
    'long_description': '[![Python Versions](https://img.shields.io/pypi/pyversions/cleopatra.png)](https://img.shields.io/pypi/pyversions/cleopatra)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MAfarrag/cleopatra.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MAfarrag/cleopatra/context:python)\n[![Documentation Status](https://readthedocs.org/projects/cleopatra/badge/?version=latest)](https://cleopatra.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/github/Serapieum-of-alex/cleopatra/branch/main/graph/badge.svg?token=gHxH7ljIC3)](https://codecov.io/github/Serapieum-of-alex/cleopatra)\n\n![GitHub last commit](https://img.shields.io/github/last-commit/MAfarrag/cleopatra)\n![GitHub forks](https://img.shields.io/github/forks/MAfarrag/cleopatra?style=social)\n![GitHub Repo stars](https://img.shields.io/github/stars/MAfarrag/cleopatra?style=social)\n\n\nCurrent release info\n====================\n\n| Name | Downloads                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Version | Platforms |\n| --- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| --- | --- |\n| [![Conda Recipe](https://img.shields.io/badge/recipe-cleopatra-green.svg)](https://anaconda.org/conda-forge/cleopatra) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/cleopatra.svg)](https://anaconda.org/conda-forge/cleopatra) [![Downloads](https://pepy.tech/badge/cleopatra)](https://pepy.tech/project/cleopatra) [![Downloads](https://pepy.tech/badge/cleopatra/month)](https://pepy.tech/project/cleopatra)  [![Downloads](https://pepy.tech/badge/cleopatra/week)](https://pepy.tech/project/cleopatra)  ![PyPI - Downloads](https://img.shields.io/pypi/dd/cleopatra?color=blue&style=flat-square) ![GitHub all releases](https://img.shields.io/github/downloads/MAfarrag/cleopatra/total) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/cleopatra.svg)](https://anaconda.org/conda-forge/cleopatra) [![PyPI version](https://badge.fury.io/py/cleopatra.svg)](https://badge.fury.io/py/cleopatra) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/cleopatra/badges/version.svg)](https://anaconda.org/conda-forge/cleopatra) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/cleopatra.svg)](https://anaconda.org/conda-forge/cleopatra) [![Join the chat at https://gitter.im/Hapi-Nile/Hapi](https://badges.gitter.im/Hapi-Nile/Hapi.svg)](https://gitter.im/Hapi-Nile/Hapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) |\n\ncleopatra - matplotlib utility package\n=====================================================================\n**cleopatra** is a matplotlib utility package\n\ncleopatra\n\n\nInstalling cleopatra\n===============\n\nInstalling `cleopatra` from the `conda-forge` channel can be achieved by:\n\n```\nconda install -c conda-forge cleopatra\n```\n\nIt is possible to list all of the versions of `cleopatra` available on your platform with:\n\n```\nconda search cleopatra --channel conda-forge\n```\n\n## Install from Github\nto install the last development to time you can install the library from github\n```\npip install git+https://github.com/MAfarrag/cleopatra\n```\n\n## pip\nto install the last release you can easly use pip\n```\npip install cleopatra==0.2.7\n```\n\nQuick start\n===========\n\n```\n  >>> import cleopatra\n```\n\n[other code samples](https://cleopatra.readthedocs.io/en/latest/?badge=latest)\n',
    'author': 'Mostafa Farrag',
    'author_email': 'moah.farag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MAfarrag/cleopatra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
