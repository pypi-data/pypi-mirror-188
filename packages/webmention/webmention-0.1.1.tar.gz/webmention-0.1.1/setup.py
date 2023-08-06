# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['webmention']
install_requires = \
['microformats>=0.0', 'requests>=2.28.2,<3.0.0', 'txtint>=0.0']

entry_points = \
{'console_scripts': ['webmention = webmention.__main__:main']}

setup_kwargs = {
    'name': 'webmention',
    'version': '0.1.1',
    'description': 'utilities to help implement Webmention sending and receiving',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
