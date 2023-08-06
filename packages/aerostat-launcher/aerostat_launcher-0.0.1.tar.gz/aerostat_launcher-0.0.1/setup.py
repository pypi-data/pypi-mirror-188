# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerostat', 'aerostat.aws', 'aerostat.core']

package_data = \
{'': ['*'], 'aerostat': ['scripts/*'], 'aerostat.aws': ['.serverless/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'questionary>=1.10.0,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['cli = aerostat.cli:main']}

setup_kwargs = {
    'name': 'aerostat-launcher',
    'version': '0.0.1',
    'description': 'A simple CLI tool to deploy your Machine Learning models to cloud, with a public API to use.',
    'long_description': '# Aerostat\n\nAerostat is a simple CLI tool to deploy your Machine Learning models to cloud, with a public API to use.\n\n## Get started\n### Installation\nThe name `Aerostat` has been used by another PyPI project, please install this package with:\n```bash\npip install git+https://github.com/vinceyyyyyy/Aerostat\n```\nMost likely you will need to run this module with `python -m` prefix since it is not included in `$PATH`.\n\nTo deploy your model, there are only three commands needed: `install`, `login`, and `deploy`.\n\n### Setup\nRun the following command, and it will install all the dependencies needed to run Aerostat.\n```bash\npython -m aerostat install\n```\n\nTo login to Aerostat, you need to run the following command:\n```bash\npython -m aerostat login\n```\nYou will be prompted to choose an existing AWS credentials, or enter a new one. The AWS account used needs to have **AdministratorAccess**. \n\n### Deploy\nTo deploy your model, you need to dump your model to a file with pickle, and run the following command:\n```bash\npython -m aerostat deploy\n```\nYou will be prompted to enter:\n- the path to your model file\n- the input columns of your model\n- the ML library used for your model\n\nOr you can provide these information as command line options like:\n```bash\npython -m aerostat deploy --model-path /path/to/model --input-columns "[\'col1\',\'col2\',\'col3\']" --python-dependencies scikit-learn\n```\n\n\n## Roadmap\n- [x] Deploy a model to AWS Lambda\n- [ ] Improve error handling, including login checks\n- [ ] Improve user interface, including rewrite prompts with Rich, use more colors and emojis\n- [ ] Return deployment info and simple test demo with HTTP GET request\n- [ ] Make it a pip installable package\n- [ ] Handle AWS authentication from the CLI\n- [ ] Support deploying to GCP',
    'author': 'Vincent Yan',
    'author_email': 'vincent.yan@blend360.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vinceyyyyyy/Aerostat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
