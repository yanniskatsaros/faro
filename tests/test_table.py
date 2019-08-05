from numpy import ndarray
from pandas import DataFrame

import faro

data = [
    ('fruit', 'id', 'in_stock', 'rating'),
    ('apple', 24, True, 5.0),
    ('orange', 34, False, 4.1),
    ('banana', 14, False, 4.9),
    ('peach', 69, True, 3.45)
]
table = faro.Table(data, header=True)

def test_constructor_no_header():
    faro.Table(data[1:], header=False)

def test_constructor_with_header():
    faro.Table(data, header=True)

def test_to_list():
    """Tests that results are returned as list of tuples"""
    results = table.to_list()
    assert(type(results) == list)
    assert(type(results[0]) == tuple)

def test_to_matrix():
    """Tests that results are returned as a numpy.ndarray"""
    results = table.to_numpy()
    assert(type(results) == ndarray)

def test_to_dict():
    """Tests that results are returned as a dict"""
    results = table.to_dict()
    assert(type(results) == dict)

def test_to_dataframe():
    """Tests that results are returned as a pandas.DataFrame"""
    results = table.to_dataframe()
    assert(type(results) == DataFrame)
