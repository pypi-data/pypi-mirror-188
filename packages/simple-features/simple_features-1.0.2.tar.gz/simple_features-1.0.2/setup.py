# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_features']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-features',
    'version': '1.0.2',
    'description': "Just some simple additions to your python experience like most 3-4 bit colors and making useful commands like time.sleep(null) and os.system('clear') more user friendly.",
    'long_description': None,
    'author': 'Stefan Dikov',
    'author_email': 'stefan.v.dikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
