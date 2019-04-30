# A simple parallel map utility

## Installation

First find a Python 3 executable.

The following step creates build a `build/` directory, which can be added
to your `PYTHONPATH`.
```
$ python setup.py build
```

To build the software into the global installation of your environment (ideally,
but not necessarily, a virtual environment), use:
```
$ pip install --no-deps .
```

## Example

```python
from parallel_map import parallel_map
parallel_map(lambda x: x**2, range(10))
```
