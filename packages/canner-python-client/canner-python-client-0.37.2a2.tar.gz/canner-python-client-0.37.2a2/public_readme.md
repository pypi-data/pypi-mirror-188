![pypi](https://img.shields.io/pypi/v/canner-python-client.svg)

# Introduction

This package provides a client interface to query Canner
a distributed SQL engine. It supports Python 3.6.x, 3.7.x and 3.8.x.

# Old package versions If needed

If you would like to download old versions which smaller than `0.37.x` ( < `0.37.x` ), please go to [cannerflow-python-client](https://pypi.org/project/cannerflow-python-client/) page.

# Installation

```
$ pip install canner-python-client
```

# Quick Start

## Client

```python
import canner
# bootstrap canner client with credentials
client = canner.client.bootstrap(
  endpoint='https://web.default.myname.apps.canner.com',
  workspace_id='444e8753-a4c0-4875-bdc0-834c79061d56',
  token='Y2xpZW50XzA0OTgzODM4LWNhZjktNGNmZi1hNDA4LWFkZDY3ZDc5MjIxNjo2N2YyNGY5OWEzYjFiZTEyZTg2MDI2MmMzNGQzZDRiYQ=='
)

# generate simple tpch query
query = client.gen_query('select * from tpch.tiny.region', data_format='list')
query.wait_for_finish()

# get all data with `get_all()` and data will be list of rows
data = query.get_all()
```

Please change your `endpoint`, `workspace_id` and `token` according to your canner web environment.

## Installing `canner-python-client` issues

### 1. Show `Couldn't find index page for 'xxx' (maybe misspelled?)` when installing dependency package `fastparquet` stage

If you're installing our `canner-python-client` by pip, and meet these message: `Couldn't find index page for 'xxx' (maybe misspelled?)`

E.g: `numpy`, `pytest-runner` followed the error `distutils.errors.DistutilsError: Could not find suitable distribution for Requirement.parse('xxxx')`,

**Solution:**
then please install these package by hand through `pip install` command, and make sure the dependency package exist on PyPI, like below:

```bash
# If you face the issue for numpy
$> pip install numpy==1.19.5 # recommend version for our package

# If you face the issue for pytest-runner
$> pip install pytest-runner==5.3.1 # recommend version for our package
```

### 2. Show `RuntimeError: Python version >= 3.x required.` when installing dependency package `fastparquet` stage in Python 3.6.x

This error may happen on installing dependency package `fastparquet` stage and occurs when `fastparquet` install `numpy` version, but the `numpy` may install latest version from `fastparquet` so it need `Python version >= 3.x` required,
Even our package `setup.py` add installing `numpy==1.19.5` or `numpy>=1.19.5` before `fastparquet`.

**Reason:** because python will download all package first, so at that time if our `pip list` not contains `numpy`, `fastparquet` not found `numpy`, so it will download by `fastparquet` rule.

**Solution:** You could install `numpy 1.19.5` version (recommend) by `pip install` before installing `canner-python-client` to prevent the issue.

```bash

$> pip install numpy==1.19.5
$> pip install canner-python-client
```

### 3. Show error for current installing numba needed numpy version and installed numpy version is incompatible

When downloading `canner-python-client` under python `3.8.x`, it will encounter `numpy` and `numba` version conflicts.

The error message will like the below (the error message for numba needed numpy version may be different on your system installed numpy version):

Here is an error message sample, your version of numba and numpy may be different on your system:

```bash
ERROR: numba 0.55.0 has requirement numpy<1.22,>=1.18, but you'll have numpy 1.22.1 which is incompatible.
```

**Solution:** you could install `numba 0.53.x` and `numpy 1.22.x` first

```bash
# Example 1:
$> pip install numba==0.53
$> pip install numpy==1.22.0
$> pip install canner-python-client

# Example 2:
$> pip install numba==0.53.1
$> pip install numpy==1.22.4
$> pip install canner-python-client
```

### 4. Show errors when python client installing dependency package "pyarrow"

When you installing `canner-python-client` under the Mac M1 platform, it will shows the errors for `ERROR: Could not build wheels for pyarrow, which is required to install pyproject.toml-based projects` when the `python version < 3.8`.
The reason is that the used dependency package `pyarrow` not have `pyarrow` wheels for M1 platform, if you would like to install `canner-python-client` successfully, please try to upgrade python version to `python 3.8.x` or not use Mac M1 platform.

```bash
...
 ERROR: Failed building wheel for pyarrow
Failed to build pyarrow
ERROR: Could not build wheels for pyarrow, which is required to install pyproject.toml-based projects
```

## Learn more

Please learn more from

1. [Canner Official Document](https://flow.cannerdata.com/)
1. [Python Client Document](https://docs.cannerdata.com/product/api_sdk/sdk/python)
