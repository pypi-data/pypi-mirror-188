# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['multimediasorter']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiohttp>=3.8.3,<4.0.0',
 'async-cache>=1.1.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'rich>=13.1.0,<14.0.0']

entry_points = \
{'console_scripts': ['multimediasorter = multimediasorter.cli:main']}

setup_kwargs = {
    'name': 'multimediasorter',
    'version': '0.0.11',
    'description': '',
    'long_description': '',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
