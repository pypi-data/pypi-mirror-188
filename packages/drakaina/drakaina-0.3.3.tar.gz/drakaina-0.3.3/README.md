# drakaina

[![image](https://img.shields.io/pypi/v/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![image](https://img.shields.io/pypi/l/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![image](https://img.shields.io/pypi/pyversions/drakaina.svg)](https://pypi.python.org/pypi/drakaina)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

❗ WIP

Module for simple RPC server implementation


## Quickstart

Drakaina may be installed via `pip` and requires Python 3.7.0 or higher :

```shell
pip install drakaina
```

A minimal Drakaina example is:

```python
from drakaina import remote_procedure
from drakaina.rpc_protocols import JsonRPCv2
from drakaina.wsgi import WSGIHandler


@remote_procedure
def my_method():
    return "Hello Bro! ✋️"


JsonRPCv2().handle({"jsonrpc": "2.0", "method": "my_method", "id": 1})
# or define WSGI application
app = WSGIHandler()
```

Drakaina may be ran with any WSGI-compliant server,
such as [Gunicorn](http://gunicorn.org).

```shell
gunicorn main:app
```


## Features

- WSGI protocol implementation
  - Compatible with simple middlewares for others wsgi-frameworks,
    like as [Werkzeug](https://palletsprojects.com/p/werkzeug/),
    [Flask](https://palletsprojects.com/p/flask/)
