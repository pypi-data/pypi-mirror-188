# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drakaina',
 'drakaina.client',
 'drakaina.contrib',
 'drakaina.contrib.django',
 'drakaina.contrib.jwt',
 'drakaina.middlewares',
 'drakaina.middlewares.openapi']

package_data = \
{'': ['*']}

extras_require = \
{'msgpack': ['msgpack>=1.0.4,<2.0.0'],
 'orjson': ['orjson>=3.8.5,<4.0.0'],
 'ujson': ['ujson>=5.7.0,<6.0.0']}

setup_kwargs = {
    'name': 'drakaina',
    'version': '0.3.3',
    'description': 'Module for simple RPC server implementation',
    'long_description': '# drakaina\n\n[![image](https://img.shields.io/pypi/v/drakaina.svg)](https://pypi.python.org/pypi/drakaina)\n[![image](https://img.shields.io/pypi/l/drakaina.svg)](https://pypi.python.org/pypi/drakaina)\n[![image](https://img.shields.io/pypi/pyversions/drakaina.svg)](https://pypi.python.org/pypi/drakaina)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n\n❗ WIP\n\nModule for simple RPC server implementation\n\n\n## Quickstart\n\nDrakaina may be installed via `pip` and requires Python 3.7.0 or higher :\n\n```shell\npip install drakaina\n```\n\nA minimal Drakaina example is:\n\n```python\nfrom drakaina import remote_procedure\nfrom drakaina.rpc_protocols import JsonRPCv2\nfrom drakaina.wsgi import WSGIHandler\n\n\n@remote_procedure\ndef my_method():\n    return "Hello Bro! ✋️"\n\n\nJsonRPCv2().handle({"jsonrpc": "2.0", "method": "my_method", "id": 1})\n# or define WSGI application\napp = WSGIHandler()\n```\n\nDrakaina may be ran with any WSGI-compliant server,\nsuch as [Gunicorn](http://gunicorn.org).\n\n```shell\ngunicorn main:app\n```\n\n\n## Features\n\n- WSGI protocol implementation\n  - Compatible with simple middlewares for others wsgi-frameworks,\n    like as [Werkzeug](https://palletsprojects.com/p/werkzeug/),\n    [Flask](https://palletsprojects.com/p/flask/)\n',
    'author': 'Aleksey Terentyev',
    'author_email': 'terentyev.a@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tau_lex/drakaina',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
