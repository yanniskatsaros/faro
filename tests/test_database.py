import pytest
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
db = faro.Database('tests')

def test_add_csv():
    """Tests adding a CSV by name to the database"""
    db.add_table('airports.csv', 'airports')

def test_add_json():
    """Tests adding a JSON by name to the database"""
    db.add_table('cars.json', 'cars')

def test_add_dataframe():
    """Tests adding a pandas.DataFrame to the database"""
    df = DataFrame(data[1:])
    df.columns = data[0]
    db.add_table(df, 'fruits')

def test_add_faro_table():
    """Tests adding a faro.Table to the database"""
    table = faro.Table(data)
    db.add_table(table, 'other_fruits')

def test_add_invalid_file():
    """Tests adding an invalid file to the database"""
    with pytest.raises(FileNotFoundError):
        db.add_table('invalid.csv', 'invalid')
