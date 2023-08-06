# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['alpha_kentaurus']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['alpha = alpha_kentaurus.main:main']}

setup_kwargs = {
    'name': 'alpha-kentaurus',
    'version': '0.1.2',
    'description': "Ah ah ah, you didn't say the magic word",
    'long_description': "## Not what you're looking for\n![nope](https://cultfilmclub.com/wp-content/uploads/2015/04/Nedry.png)  \n[Ah ah ah, you didn't say the magic word](https://www.youtube.com/watch?v=RfiQYRn7fBg)  \n",
    'author': 'nope',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
