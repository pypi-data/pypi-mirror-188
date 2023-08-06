# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytatsu']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'pybmtool>=0.1.4,<0.2.0']

entry_points = \
{'console_scripts': ['tatsu = pytatsu.__main__:cli']}

setup_kwargs = {
    'name': 'pytatsu',
    'version': '0.1.5',
    'description': "A Python library/CLI tool for requesting and saving SHSH blobs from Apple's Tatsu signing server API.",
    'long_description': "# pytatsu\n\n## A Python library/CLI tool for requesting and saving SHSH blobs from Apple's Tatsu signing server API.\n",
    'author': 'Cryptiiiic',
    'author_email': 'liamwqs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cryptiiiic/pytatsu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
