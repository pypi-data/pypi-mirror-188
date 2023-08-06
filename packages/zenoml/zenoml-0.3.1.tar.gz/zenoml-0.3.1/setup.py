# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeno', 'zeno.classes', 'zeno.data_pipeline']

package_data = \
{'': ['*'],
 'zeno': ['frontend/*', 'frontend/build/*', 'frontend/build/assets/*']}

install_requires = \
['fastapi>=0.75,<0.90',
 'inquirerpy>=0.3.4,<0.4.0',
 'methodtools>=0.4.5,<0.5.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'pandas>=1.4.0,<2.0.0',
 'pathos>=0.3.0,<0.4.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'setuptools>=67.0.0,<68.0.0',
 'tomli>=2.0.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'types-requests>=2.28.11,<3.0.0',
 'types-setuptools>=65.4.0,<66.0.0',
 'types-tqdm>=4.64.7,<5.0.0',
 'uvicorn>=0.17.5,<0.21.0',
 'websockets>=10.2,<11.0']

entry_points = \
{'console_scripts': ['zeno = zeno.runner:command_line']}

setup_kwargs = {
    'name': 'zenoml',
    'version': '0.3.1',
    'description': 'Interactive Evaluation Framework for Machine Learning',
    'long_description': '<img src="./zeno.png" width="250px"/>\n\n[![PyPI version](https://badge.fury.io/py/zenoml.svg)](https://badge.fury.io/py/zenoml)\n![Github Actions CI tests](https://github.com/zeno-ml/zeno/actions/workflows/test.yml/badge.svg)\n![Github Actions Docs build](https://github.com/zeno-ml/zenoml.com/actions/workflows/docs.yml/badge.svg)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Join the chat at https://gitter.im/zeno-ml-eval/community](https://badges.gitter.im/zeno-ml-eval/community.svg)](https://gitter.im/zeno-ml-eval/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\nZeno is a general-purpose framework for evaluating machine learning models.\nIt combines a **Python API** with an **interactive UI** to allow users to discover, explore, and analyze the performance of their models across diverse use cases.\nZeno can be used for any data type or task with [modular views](https://zenoml.com/docs/views/) for everything from object detection to audio transcription.\n\n## Quickstart\n\nInstall the Zeno Python package from PyPI:\n\n```bash\npip install zenoml\n```\n\n### Command Line\n\nTo get started, run the following command to initialize a Zeno project. It will walk you through creating the `zeno.toml` configuration file:\n\n```bash\nzeno init\n```\n\nThen run `zeno zeno.toml`.\n\n### Jupyter Notebook\n\nYou can also run Zeno directly from Jupyter notebooks or lab. The `zeno` command takes a dictionary of configuration options as input. See [the docs](https://zenoml.com/docs/configuration) for a full list of options. In this example we pass the minimum options for exploring a non-tabular dataset:\n\n```python\nimport pandas as pd\nfrom zeno import zeno\n\ndf = pd.read_csv("/path/to/metadata/file.csv")\n\nzeno({\n    "metadata": df, # Pandas DataFrame with a row for each instance\n    "view": "audio-transcription", # The type of view for this data/task\n    "data_path": "/path/to/raw/data/", # The folder with raw data (images, audio, etc.)\n    "data_column": "id" # The column in the metadata file that contains the relative paths of files in data_path\n})\n\n```\n\n## Learn More\n\nCheck out examples and additional documentation:\n\n- [Introduction](https://zenoml.com/docs/intro) - Learn more about Zeno.\n- [Quickstart](http://zenoml.com/docs/quickstart) - Setup Zeno with your own data and models.\n- [Documentation & API](http://zenoml.com/docs/intro) - Full documentation and API reference.\n',
    'author': 'Ángel Alexander Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zenoml.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<=3.11',
}


setup(**setup_kwargs)
