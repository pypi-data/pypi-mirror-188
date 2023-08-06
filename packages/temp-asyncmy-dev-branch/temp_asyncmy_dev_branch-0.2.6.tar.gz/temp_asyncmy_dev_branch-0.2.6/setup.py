# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncmy', 'asyncmy.constants', 'asyncmy.replication']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'temp-asyncmy-dev-branch',
    'version': '0.2.6',
    'description': 'asyncmy 0.2.6 Dev Branch',
    'long_description': '# asyncmy 0.2.6 Dev Branch\n\nTemporary package created to fix the asyncy 0.2.5 bug\n\n## License\n\nThis project is licensed under the [Apache-2.0](./LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/long2ice/asyncmy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
