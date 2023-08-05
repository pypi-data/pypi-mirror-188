# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambdamoo_db']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'cattrs>=22.2.0,<23.0.0']

setup_kwargs = {
    'name': 'lambdamoo-db',
    'version': '0.1.0',
    'description': 'Parser for LambdaMOO databases',
    'long_description': '',
    'author': 'Katelyn Gigante',
    'author_email': 'clockwork.singularity@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
