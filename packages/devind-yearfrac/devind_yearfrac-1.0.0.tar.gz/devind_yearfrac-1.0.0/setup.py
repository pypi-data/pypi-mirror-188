# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devind_yearfrac']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'devind-yearfrac',
    'version': '1.0.0',
    'description': 'Daycount methods to compute date differences in year units',
    'long_description': '# devind_yearfrac\n\n[![CI](https://github.com/devind-team/devind_yearfrac/workflows/Release/badge.svg)](https://github.com/devind-team/devind_yearfrac/actions)\n[![PyPI version](https://badge.fury.io/py/devind_yearfrac.svg)](https://badge.fury.io/py/devind_yearfrac)\n[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](https://opensource.org/licenses/MIT)\n\nThis is a fork of [`yearfrac`](https://github.com/kmedian/yearfrac) for use in\n[`xlsx_evaluate`](https://github.com/devind-team/xlsx_evaluate).\nThis fork mainly supports `poetry` and newer versions of Python.\n\n## Installation\n```\npoetry add devind_yearfrac\n```\n',
    'author': 'Ulf Hamster',
    'author_email': '554c46@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/devind-team/devind_yearfrac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
