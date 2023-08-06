# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regreplace']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'regreplace',
    'version': '0.1.4',
    'description': 'Replace named regex group by a given string',
    'long_description': None,
    'author': 'Gwang-Jin Kim',
    'author_email': 'gwang.jin.kim.phd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
