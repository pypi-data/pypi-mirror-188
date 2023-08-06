# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reconcile_core', 'reconcile_core.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'reconcile-core',
    'version': '0.1.1',
    'description': 'Reconciliation library',
    'long_description': 'None',
    'author': 'Simon Andrieux',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
