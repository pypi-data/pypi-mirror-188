# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testbench_sardine']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'requests>=2.28.2,<3.0.0',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'testbench-sardine',
    'version': '1.0.0',
    'description': 'Personal testbench for trying out stuff.',
    'long_description': '# Testbench Sardine\n\nPersonal testbench for trying out stuff.\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim@trallnag.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/trallnag/testbench-sardine',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
