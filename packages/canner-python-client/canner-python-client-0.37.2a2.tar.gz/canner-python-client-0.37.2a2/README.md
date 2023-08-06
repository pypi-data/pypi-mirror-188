![pypi](https://img.shields.io/pypi/v/canner-python-client.svg)

# Introduction

This package provides a client interface to query Canner
a distributed SQL engine. It supports Python 3.6.x, 3.7.x, and 3.8.x.

# Installation

```
$ pip install canner-python-client
```

# Quick Start

## Client

As client to use the `canner-python-client` package.

### Using canner user account permission to access

We use your canner **user account** to access by `token` , however the access dataset permission followed by your **user account** role.
So if your **user account** role is **data consumer**, then only semantic layer dataset could do the query, if not, you could query all dataset in the `workspace_id` you given.

```python
import canner

client = canner.client.bootstrap(
    endpoint=ENDPOINT
    workspace_id=WORKSPACE_ID,
    token=CANNER_PERSONAL_ACCESS_TOKEN
)

# generate simple tpch query
query = client.gen_query('select * from tpch.tiny.region', data_format='list')
query.wait_for_finish()

# get all data with `get_all()` and data will be list of rows
data = query.get_all()
```

Please change your `endpoint`, `workspace_id` and `token` according to your canner web environment.

### Using jupyter user permission to access

We could also use **jupyter user** to access by `X-CANNERFLOW-SECRET` , however our jupyter user is **data consumer** role, so only semantic layer dataset could do the query.

```python
client = canner.client.bootstrap(
    endpoint=ENDPOINT
    workspace_id=WORKSPACE_ID,
    headers={
        'X-CANNERFLOW-SECRET': JUPYTER_SECRET,
        'X-CANNERFLOW-WORKSPACE-ID': WORKSPACE_ID
    }
)
```

Please change your `endpoint`, `workspace_id` according to your canner web environment.
The `X-CANNERFLOW-SECRET` value, you could trace our project to get it for testing.

# Development Need

If you would like to download the source code and develop new feature or fix bug, please follow the guide below to build development environment.

# Prerequisite

Before you build development environment, please make sure we prepared the python version we supported and [poetry](https://python-poetry.org/) package which the python package and dependency management tools.

## Python version

We support python version `3.6.x`, `3.7.x` and `3.8.x`, if you use the [pyenv](https://github.com/pyenv/pyenv) to management different python version, please make sure you have switch to the version we supported.

## 1. Install Poetry

```sh
$> pip install poetry
$> poetry about

Poetry - Package Management for Python

Poetry is a dependency manager tracking local dependencies of your projects and libraries.
See https://github.com/python-poetry/poetry for more information.
```

## 2. Setup virtual environment and install packages by poetry

Using the poetry to build virtual environment and install the required package which `pyproject.toml` records.

```sh
$> cd canner-python-client
canner-python-client $> poetry install      # install development required packages, will update poetry.lock and create .venv directory
canner-python-client $> poetry shows        # show the required packages installed
canner-python-client $> poetry shows --tree # check the packages installed with dependencies
canner-python-client $> poetry shell        # enter virtual environments
(.venv) canner-python-client $>
```

## 3. Run testing files to test results

### 3.1 Setup Environment variable.

The tests code put int `tests/` and you need to setup three environment variable, you could check the meaning from [Development - Python Client](https://flow.cannerdata.com/docs/integration/development_python).

There are two method you could setup `WORKSPACE_ID`, `ENDPOINT` and `CANNER_PERSONAL_ACCESS_TOKEN`.

#### Setup by `pytest.ini`

This is pytest environment setup way that change the environment variable by edit `env` key in `pytest.ini`, these value is **example** (you need to change your value).

```ini
[pytest]
env =
    ENDPOINT=http://localhost:3000/web
    WORKSPACE_ID=9abc63f8-50bb-46a3-aea5-804b6d0d3fa3
    CANNER_PERSONAL_ACCESS_TOKEN=Y2xpZW50Xzk5ODZmYjMyLTUyYTItNGE5Mi05ZDkxLTFlMzdjNzhiMGE0NjplNmQ2OWQ0ZDJmODc3ZWQwOGI2ZTQyNTk0ZmYxZDM0Mg=
```

If you removed the `pytest.ini` for some reason or the file has disappear, your could use the normal `export` way to do, please see next part.

#### Setup by `export`

Here is another normal way if the `pytest.ini` not exist or you would like to test our package on PyPI by pip install.
The next is **example** (you need to change your value).

```sh
export WORKSPACE_ID="2fae9bf7-a883-4f25-9566-c0d379c44440"
export ENDPOINT="http://localhost:3000"
export CANNER_PERSONAL_ACCESS_TOKEN="Y2xpZW50Xzk5ODZmYjMyLTUyYTItNGE5Mi05ZDkxLTFlMzdjNzhiMGE0NjplNmQ2OWQ0ZDJmODc3ZWQwOGI2ZTQyNTk0ZmYxZDM0Mg="
```

#### Change for Github CI Action workflow used

Because the `canner-python-client` also supported run unit testing on Github Action CI, when you created PR on Github followed your developing feature, you will
see the Github Action run and practice unit testing workflow.

Therefore, when you would like to change these environment variable of Github Action CI, you could go to settings > secretes and update the `ENDPOINT`, `WORKSPACE_ID`
and `CANNER_PERSONAL_ACCESS_TOKEN` and run Github Action workflow again.

### 3.2 Run tests by `pytest` command

You could run test cases by `pytest`.

```sh
(.venv) canner-python-client $> pytest
# Run pytest to test Specific file.
(.venv) canner-python-client $> pytest tests/test_client.py
```

Or you could run tests by python.

```sh
(.venv) canner-python-client $> python -m pytest tests
```

## 4. Publish

After you finished the development and would like to publish to remote repository like [pypi](https://pypi.org/project/canner-python-client/).

```sh
# Update version in __init__.py
vim canner/__init__.py
# Removed old distribution
rm -rf dist
# Build source distribution (please follow the more detail about setuptools document)
python setup.py sdist
# upload to pypi and type account & password
twine upload dist/*
```

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
$> pip install pytest-runner==5.3.0 # recommend version for our package
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
