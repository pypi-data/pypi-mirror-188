# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite',
 'cognite.experimental',
 'cognite.experimental._api',
 'cognite.experimental.data_classes',
 'cognite.experimental.data_classes.model_hosting',
 'cognite.experimental.data_classes.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk>=5,<6',
 'pandas>=1.1.5',
 'regex>=2020.11.13,<2023',
 'responses>=0.13.3,<0.14.0',
 'sympy>=1.3.0,<2.0.0',
 'typing-extensions>=3.7.4,<5']

extras_require = \
{'geopandas': ['geopandas>=0.10.0', 'shapely>=1.7.0']}

setup_kwargs = {
    'name': 'cognite-sdk-experimental',
    'version': '0.110.0',
    'description': 'Experimental additions to the Python SDK',
    'long_description': 'None',
    'author': 'Sander Land',
    'author_email': 'sander.land@cognite.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
