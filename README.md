# A simple parallel map utility

## Installing

First find a Python 3 executable.

### From PyPI

```
$ pip install parallel_map
```

### Manual Install

The following step creates build a `build/` directory, which can be added
to your `PYTHONPATH`.
```
$ python setup.py build
```

To build the software into the global installation of your environment (ideally,
but not necessarily, a virtual environment), use:
```
$ pip install .
```

## Example

```python
from parallel_map import parallel_map
parallel_map(lambda x: x**2, range(10))
```

## License

Apache License 2.0, see LICENSE.txt.

This repository contains a stand-alone module of a useful parallel mapping
feature, originally written by Taylor R. Campbell as part of the Venture
project.
