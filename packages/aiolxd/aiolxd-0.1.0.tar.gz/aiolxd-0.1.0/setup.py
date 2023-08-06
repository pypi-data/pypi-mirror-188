# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiolxd']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'aiolxd',
    'version': '0.1.0',
    'description': 'AsyncIO LXD API for Python 3',
    'long_description': 'None',
    'author': 'Egor Ternovoy',
    'author_email': 'cofob@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cofob/aiolxd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
