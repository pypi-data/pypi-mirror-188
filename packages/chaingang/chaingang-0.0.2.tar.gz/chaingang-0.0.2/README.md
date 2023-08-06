# ChainGang: python class decorator that adds selection chaining
-----------------
[![PyPI Latest Release](https://img.shields.io/pypi/v/chaingang.svg)](https://pypi.org/project/chaingang/)
![Tests](https://github.com/eddiethedean/chaingang/actions/workflows/tests.yml/badge.svg)

## What is it?

**ChainGang** is a Python package that provides a class decorator function that adds selection chaining to classes with nested items.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/eddiethedean/chaingang

```sh
# PyPI
pip install chaingang
```

## Dependencies


## Example
```sh
from chaingang import selection_chaining

# decorate a class with nested items
@selection_chaining
class ChainList(list):
    ...

cl = ChainList([[1, 2, 3], [4, 5, 6]])

# select inner item with comma separated indexes
cl[1, 2] -> 6
# same as bracket chaining
cl[1][2] -> 6

# set inner item value
cl[1, 2] = 100
cl -> [[1, 2, 3], [4, 5, 100]]

# delete inner item
del cl[1, 1]
cl -> [[1, 2, 3], [4, 100]]
```