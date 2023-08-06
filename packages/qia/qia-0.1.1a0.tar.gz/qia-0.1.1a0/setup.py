# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qia']

package_data = \
{'': ['*']}

install_requires = \
['appium-python-client>=2.8.1,<3.0.0',
 'behave>=1.2.6,<2.0.0',
 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'qia',
    'version': '0.1.1a0',
    'description': 'Automated testing tool for Web and Mobile with Python.',
    'long_description': '# qia\nAutomated testing tool for Web and Mobile with Python.\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
