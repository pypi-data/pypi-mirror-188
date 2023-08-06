# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sapiadapter']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'sapiadapter',
    'version': '0.38.28',
    'description': '',
    'long_description': '',
    'author': 'Zafar Iqbal',
    'author_email': 'zaf@sparc.space',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
