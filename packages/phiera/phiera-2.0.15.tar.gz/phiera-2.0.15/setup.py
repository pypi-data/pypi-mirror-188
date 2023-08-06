# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phiera']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'phiera',
    'version': '2.0.15',
    'description': 'a python hiera parser',
    'long_description': 'Phiera\n---\n\n[![codecov](https://codecov.io/gh/Nike-Inc/phiera/branch/master/graph/badge.svg?token=J9slc2blRx)](https://codecov.io/gh/Nike-Inc/phiera)\n[![Test](https://github.com/Nike-Inc/phiera/actions/workflows/python-test.yaml/badge.svg)](https://github.com/Nike-Inc/phiera/actions/workflows/python-test.yaml)\n[![PyPi Release](https://github.com/Nike-Inc/phiera/actions/workflows/python-build.yaml/badge.svg)](https://github.com/Nike-Inc/phiera/actions/workflows/python-build.yaml)\n![License](https://img.shields.io/pypi/l/phiera)\n![Python Versions](https://img.shields.io/pypi/pyversions/phiera)\n![Python Wheel](https://img.shields.io/pypi/wheel/phiera)\n\nPhiera is a fork of [Piera](https://github.com/b1naryth1ef/pierahttps://github.com/b1naryth1ef/piera), a lightweight, pure-Python [Hiera](http://docs.puppetlabs.com/hiera/) parser. Piera was originally built to provide Python tooling access to Puppet/Hiera configurations. The original Piera is currently not feature complete; lacking some less-used interpolation and loading features.\n\nTable of content\n* [Why](#why)\n* [Installation](#installation)\n* [Usage](#usage)\n* [Unit Tests](#tests)\n\n# <a name="why"></a> Why?:\n\nPiera/Phiera generalizes Puppet Hiera\'s hierarchical storage system; making a simple, very flexible, abstracted, and DRY mechanism for managing complex configuration data available to a broad set of tooling and applicable to a broad set of problems.\n\nPhiera builds on the original Piera work, adding:\n  \n  - Python3 compatibility\n  - Support for deep merging\n  - Support for configuration as a dict\n\n# <a name="installation"></a> Installation:\n\n### From PyPi:\n```shell script\npip install phiera\n```\n\n### From GitHub:\n```shell script\npip install git+https://github.com/Nike-Inc/phiera#egg=phiera\n```\n\n\n### Manually\n\n```bash\ngit clone git@github.com/Nike-Inc/phiera.git\ncd phiera\npython setup.py install\n```\n\n# <a name="usage"></a> Usage:\n\n```python\nimport phiera\n\nh = phiera.Hiera("my_hiera.yaml")\n\n# You can use phiera to simply interact with your structured Hiera data\n\n# key: \'value\'\nassert h.get("key") == "value"\n\n# key_alias: \'%{alias(\'key\')}\'\nassert h.get("key_alias") == "value"\n\n# key_hiera: \'OHAI %{hiera(\'key_alias\')}\'\nassert h.get("key_hiera") == "OHAI value"\n\n# Give phiera context\nassert h.get("my_context_based_key", name=\'test01\', environment=\'qa\') == "context is great!"\n```\n\n# <a name="tests"></a> Unit Tests:\n\n```bash\npoetry run pytest --cov-report=html --cov=phiera --cov-fail-under=80 tests/\n```\n',
    'author': 'Andrei Zbikowski, Rob King',
    'author_email': None,
    'maintainer': 'Mohamed Abdul Huq Ismail',
    'maintainer_email': 'Abdul.Ismail@nike.com',
    'url': 'https://github.com/Nike-Inc/phiera',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
