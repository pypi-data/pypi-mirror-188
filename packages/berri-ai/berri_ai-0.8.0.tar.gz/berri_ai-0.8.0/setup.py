# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berri_ai']

package_data = \
{'': ['*']}

install_requires = \
['pipreqs>=0.4.11,<0.5.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'berri-ai',
    'version': '0.8.0',
    'description': '',
    'long_description': None,
    'author': 'Team Berri',
    'author_email': 'clerkieai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
