# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automate',
 'automate.builder',
 'automate.database',
 'automate.model',
 'automate.tasks',
 'automate.utils']

package_data = \
{'': ['*'], 'automate.database': ['queries/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'coloredlogs>=10.0,<11.0',
 'fabric>=2.5,<3.0',
 'invoke>=1.3,<2.0',
 'keyring>=21.1.0,<22.0.0',
 'patchwork>=1.0,<2.0',
 'prompt_toolkit>=3.0,<4.0',
 'pydantic>=1.2,<2.0',
 'requests>=2.22,<3.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'setproctitle>=1.1.10,<2.0.0',
 'tabulate>=0.8.6,<0.9.0']

extras_require = \
{'postgres': ['python-dotenv>=0.10.5,<0.11.0',
              'pydot>=1.4.1,<2.0.0',
              'jinjasql>0.1.7',
              'psycopg2-binary>=2.8.6,<3.0.0']}

entry_points = \
{'console_scripts': ['automate = automate.main:program.run',
                     'automate-run = automate.main:program_run.run']}

setup_kwargs = {
    'name': 'board-automate',
    'version': '0.2.2',
    'description': 'Automate remote exection on linux based embedded boards',
    'long_description': 'None',
    'author': 'Christoph Gerum',
    'author_email': 'christoph.gerum@uni-tuebingen.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>3.7.1,<4.0',
}


setup(**setup_kwargs)
