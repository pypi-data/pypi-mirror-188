# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colipy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'colipy-cli',
    'version': '0.1.1.dev1',
    'description': 'Colipy is a command line ui library for python.',
    'long_description': '# Colipy\nColipy is a command line ui library for python.',
    'author': 'Johannes Lübke',
    'author_email': '60359335+johannes-luebke@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/johannes-luebke/colipy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
