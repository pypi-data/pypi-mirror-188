# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mydstools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mydstools',
    'version': '0.1.0',
    'description': 'Data Science Toolbox',
    'long_description': '# mydstools\n\nData Science Toolbox\n\n## Installation\n\n```bash\n$ pip install mydstools\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`mydstools` was created by Antonio Buzzelli. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`mydstools` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Antonio Buzzelli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
