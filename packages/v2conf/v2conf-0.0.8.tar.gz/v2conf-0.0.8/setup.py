# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['v2conf']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'jdatetime>=4.1.0,<5.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['v2conf = v2conf.__main__:main']}

setup_kwargs = {
    'name': 'v2conf',
    'version': '0.0.8',
    'description': 'V2Conf helps you build V2Ray Config file automatically and evaluate and change config rules based on outbounds performances.',
    'long_description': 'None',
    'author': 'Mahyar Mahdavi',
    'author_email': 'Mahyar@Mahyar24.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Mahyar24/V2Conf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
