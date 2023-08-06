# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['potyk_doc', 'potyk_doc.translation']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=3.0.0,<4.0.0',
 'docxtpl>=0.16.4,<0.17.0',
 'jinja2xlsx>=1,<2',
 'pdfkit>=1.0.0,<2.0.0',
 'potyk-lib>=0.6,<0.7']

setup_kwargs = {
    'name': 'potyk-doc',
    'version': '0.8.4',
    'description': '',
    'long_description': None,
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
