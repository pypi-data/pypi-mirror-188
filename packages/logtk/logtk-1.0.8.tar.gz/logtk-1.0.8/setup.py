# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtk', 'logtk.logger', 'logtk.loguru_logger']

package_data = \
{'': ['*']}

install_requires = \
['colortk==1.0.0', 'loguru==0.6.0']

setup_kwargs = {
    'name': 'logtk',
    'version': '1.0.8',
    'description': 'logging toolkit',
    'long_description': '',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
