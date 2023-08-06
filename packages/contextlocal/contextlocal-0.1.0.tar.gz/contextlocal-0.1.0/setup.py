# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextlocal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextlocal',
    'version': '0.1.0',
    'description': 'Useful wrappers around contextvars extracted from Werkzeug',
    'long_description': '# Context Locals\n\nExtract the context local functionality from [Werkzeug](https://github.com/pallets/werkzeug).\n\n## Usage\n\nPlease see the documenation at https://werkzeug.palletsprojects.com/en/2.2.x/local/',
    'author': 'Maxwell Koo',
    'author_email': 'mjkoo90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
