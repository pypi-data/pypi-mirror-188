# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meshemy', 'meshemy.blender', 'meshemy.cookbook', 'meshemy.utility']

package_data = \
{'': ['*']}

install_requires = \
['bpy>=3.4.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'open3d==0.16.0',
 'pydantic-numpy>=1.3.0,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pymeshfix>=0.16.2,<0.17.0']

setup_kwargs = {
    'name': 'meshemy',
    'version': '0.3.0',
    'description': 'Developer friendly suite for manipulating mesh',
    'long_description': '# Meshemy: Python toolbelt for manipulating mesh\nConsolidation package for manipulating mesh. Comes with cookbook models from each package\n\n## Installation\n```shell\npip install meshemy\n```\nUse it in your poetry package\n```shell\npoetry add meshemy\n```\n',
    'author': 'caniko',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11.0',
}


setup(**setup_kwargs)
