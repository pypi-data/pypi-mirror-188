# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tunneltop']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tunneltop = tunneltop:main']}

setup_kwargs = {
    'name': 'tunneltop',
    'version': '0.1.0',
    'description': 'A top-like tunnel manager',
    'long_description': '# tunneltop\na tunnel manager in the familiar top style\n',
    'author': 'terminaldwelelr',
    'author_email': 'devi@terminaldweller.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/terminaldweller/tunneltop',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
