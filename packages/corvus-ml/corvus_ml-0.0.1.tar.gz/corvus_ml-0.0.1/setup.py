# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corvus']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9',
 'jackdaw-ml>=0.0.5',
 'rich>=13,<14',
 'setuptools>=67.0.0',
 'tomli-w==1.0.0',
 'tomli==2.0.1']

entry_points = \
{'console_scripts': ['corvus = corvus:cli']}

setup_kwargs = {
    'name': 'corvus-ml',
    'version': '0.0.1',
    'description': 'Search ShareableAI Models',
    'long_description': "# Corvus - Search ShareableAI Models\n\nCorvus is a CLI tool that wraps the Searcher from [Jackdaw](https://github.com/shareableai/jackdaw). Designed for interactive and programmatic access to models saved via the ShareableAI toolkit.\n## Usage\n\n### Set API Key\n```bash\ncorvus set api_key\n```\nFollow the interactive prompt - this helps avoid having the API Key visible within the terminal history.\n\n### List Models\n\n#### Local Models\n```bash\ncorvus list --local\n```\n\n#### Remote Models\nRequires an API Key to be set\n```bash\ncorvus list --remote\n```\n\n#### Search\nSearches for all models in the Jackdaw repo on the main branch.\n```bash\ncorvus list --repo jackdaw --branch main\n```\n\nSearch for all models on the main branch of any repo;\n```bash\ncorvus list --branch main\n```\n\nSearch for all models on feature branches;\n```bash\ncorvus list --repo 'feat/%'\n```\n\n",
    'author': 'Lissa Hyacinth',
    'author_email': 'lissa@shareableai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
