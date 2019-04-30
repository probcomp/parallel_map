# Copyright (c) 2019 MIT Probabilistic Computing Project.
# See LICENSE.txt

from parallel_map import parallel_map

def test_lambda_simple():
    result = parallel_map(lambda i: i**2, range(10))
    assert result == list(map(lambda i: i**2, range(10)))
