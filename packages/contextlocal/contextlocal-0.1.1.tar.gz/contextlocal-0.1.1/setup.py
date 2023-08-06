# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextlocal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextlocal',
    'version': '0.1.1',
    'description': 'Useful wrappers around contextvars extracted from Werkzeug',
    'long_description': '# Context Locals\n\nExtract the context local functionality from [Werkzeug](https://github.com/pallets/werkzeug).\n\nThis is generally useful for a variety of contexts, where you may not want to include a full WSGI library.\n\n## Usage\n\nPlease see the documenation at https://werkzeug.palletsprojects.com/en/latest/local/\n\n## License\n\nThis is derived from Werkzeug with minimal modifications, and is under the same BSD 3-Clause license.\n\nPlease see the `LICENSE` file for details.\n',
    'author': 'Maxwell Koo',
    'author_email': 'mjkoo90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mjkoo/contextlocal',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
