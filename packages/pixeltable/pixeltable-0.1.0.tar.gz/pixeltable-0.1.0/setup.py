# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pixeltable',
 'pixeltable.functions',
 'pixeltable.functions.pil',
 'pixeltable.tests',
 'pixeltable.utils']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.1,<3.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'ftfy>=6.1.1,<7.0.0',
 'hnswlib>=0.6.2,<0.7.0',
 'jmespath>=1.0.1,<2.0.0',
 'numpy>=1.24.1,<2.0.0',
 'opencv-python-headless>=4.7.0.68,<5.0.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'regex>=2022.10.31,<2023.0.0',
 'sqlalchemy-utils>=0.39.0,<0.40.0',
 'sqlalchemy>=1.4.41,<2.0.0',
 'tensorflow>=2.11.0,<3.0.0',
 'torch>=1.13.1+cpu,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{':python_version >= "3.9" and python_version < "3.11"': ['tensorflow-io-gcs-filesystem>=0.28.0,<0.29.0']}

setup_kwargs = {
    'name': 'pixeltable',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Pixeltable\n\nPixeltable is a Python library that exposes image and video data via a table interface.\n',
    'author': 'Marcel Kornacker',
    'author_email': 'marcelk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
