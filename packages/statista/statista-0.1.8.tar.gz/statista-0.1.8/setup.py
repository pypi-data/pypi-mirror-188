# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statista']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'statista',
    'version': '0.1.8',
    'description': 'statistics package',
    'long_description': '[![Python Versions](https://img.shields.io/pypi/pyversions/statista.png)](https://img.shields.io/pypi/pyversions/statista)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MAfarrag/earth2observe.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MAfarrag/earth2observe/context:python)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/MAfarrag/earth2observe.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MAfarrag/earth2observe/alerts/)\n\n\n[![codecov](https://codecov.io/gh/Serapieum-of-alex/statista/branch/main/graph/badge.svg?token=GQKhcj2pFK)](https://codecov.io/gh/Serapieum-of-alex/statista)\n![GitHub last commit](https://img.shields.io/github/last-commit/MAfarrag/statista)\n![GitHub forks](https://img.shields.io/github/forks/MAfarrag/statista?style=social)\n![GitHub Repo stars](https://img.shields.io/github/stars/MAfarrag/statista?style=social)\n\n\nCurrent release info\n====================\n\n| Name | Downloads                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Version | Platforms |\n| --- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| --- | --- |\n| [![Conda Recipe](https://img.shields.io/badge/recipe-statista-green.svg)](https://anaconda.org/conda-forge/statista) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/statista.svg)](https://anaconda.org/conda-forge/statista) [![Downloads](https://pepy.tech/badge/statista)](https://pepy.tech/project/statista) [![Downloads](https://pepy.tech/badge/statista/month)](https://pepy.tech/project/statista)  [![Downloads](https://pepy.tech/badge/statista/week)](https://pepy.tech/project/statista)  ![PyPI - Downloads](https://img.shields.io/pypi/dd/statista?color=blue&style=flat-square) ![GitHub all releases](https://img.shields.io/github/downloads/MAfarrag/statista/total) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/statista.svg)](https://anaconda.org/conda-forge/statista) [![PyPI version](https://badge.fury.io/py/statista.svg)](https://badge.fury.io/py/statista) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/statista/badges/version.svg)](https://anaconda.org/conda-forge/statista) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/statista.svg)](https://anaconda.org/conda-forge/statista) [![Join the chat at https://gitter.im/Hapi-Nile/Hapi](https://badges.gitter.im/Hapi-Nile/Hapi.svg)](https://gitter.im/Hapi-Nile/Hapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) |\n\nstatista - Statistics package\n=====================================================================\n**statista** is a statistics package\n\nstatista\n\nMain Features\n-------------\n  - Statistical Distributions (GEV/GUMBL)\n  - Parameter estimation Lmoments/ML/MOM\n  - One-at-time (O-A-T) Sensitivity analysis.\n  - Sobol visualization\n  - Statistical Metrics\n\nFuture work\n-------------\n  - More distributions\n\n\nInstalling statista\n===============\n\nInstalling `statista` from the `conda-forge` channel can be achieved by:\n\n```\nconda install -c conda-forge statista\n```\n\nIt is possible to list all of the versions of `statista` available on your platform with:\n\n```\nconda search statista --channel conda-forge\n```\n\n## Install from Github\nto install the last development to time you can install the library from github\n```\npip install git+https://github.com/MAfarrag/statista\n```\n\n## pip\nto install the last release you can easly use pip\n```\npip install statista==0.1.8\n```\n\nQuick start\n===========\n\n```\n  >>> import statista\n```\n\n[other code samples](https://statista.readthedocs.io/en/latest/?badge=latest)\n',
    'author': 'Mostafa Farrag',
    'author_email': 'moah.farag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MAfarrag/statista',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.15',
}


setup(**setup_kwargs)
