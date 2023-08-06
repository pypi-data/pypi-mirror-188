# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pheval_exomiser',
 'pheval_exomiser.post_process',
 'pheval_exomiser.prepare',
 'pheval_exomiser.run',
 'pheval_exomiser.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'docker>=6.0.1,<7.0.0',
 'google>=3.0.0,<4.0.0',
 'oaklib>=0.1.55,<0.2.0',
 'pandas>=1.5.2,<2.0.0',
 'phenopackets>=2.0.2,<3.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'pyserde>=0.9.7,<0.10.0']

entry_points = \
{'console_scripts': ['pheval-exomiser = pheval_exomiser.cli:main'],
 'pheval.plugins': ['exomiser = pheval_exomiser.runner:ExomiserPhEvalRunner']}

setup_kwargs = {
    'name': 'pheval-exomiser',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Exomiser Runner for PhEval\n\nThis is the Exomiser plugin for PhEval. Highly experimental. Do not use.\n\n## Developers\n\nWarning, the `pheval` library is currently included as a file reference in the toml file.\n\n```\npheval = { path = "/Users/matentzn/ws/pheval" }\n```\n\nThis will change when pheval is published on pypi.\n\n',
    'author': 'Yasemin Bridges',
    'author_email': 'y.bridges@qmul.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
