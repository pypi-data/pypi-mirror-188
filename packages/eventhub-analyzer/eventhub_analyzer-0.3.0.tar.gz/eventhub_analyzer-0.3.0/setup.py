# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventhub_analyzer']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.14.1,<13.0.0',
 'click>=8.1.3,<9.0.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'texttable>=1.6.7,<2.0.0']

entry_points = \
{'console_scripts': ['eventhub-analyzer = eventhub_analyzer.main:cli']}

setup_kwargs = {
    'name': 'eventhub-analyzer',
    'version': '0.3.0',
    'description': '',
    'long_description': '# Event Hub Analyzer\n',
    'author': 'Stefan Hudelmaier',
    'author_email': 'stefan.hudelmaier@device-insight.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
