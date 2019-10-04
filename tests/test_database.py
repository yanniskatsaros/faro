import os, pytest
import sqlite3
from numpy import ndarray
from pandas import DataFrame

import faro

TEST_PATH = os.path.dirname(__file__)

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
    file = os.path.join(TEST_PATH, 'airports.csv')
    db.add_table(file, 'airports')

def test_add_json():
    """Tests adding a JSON by name to the database"""
    file = os.path.join(TEST_PATH, 'cars.json')
    db.add_table(file, 'cars')

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
        file = os.path.join(TEST_PATH, 'invalid.csv')
        db.add_table(file, 'invalid')

def test_export_sqlite():
    """Tests saving the database to disk"""
    DB_PATH = os.path.join(TEST_PATH, 'test.db')
    db.to_sqlite(DB_PATH)

    assert os.path.exists(DB_PATH)

    # cleanup
    os.remove(DB_PATH)

def test_import_sqlite():
    """Test loading a database from disk"""
    path = os.path.join(TEST_PATH, 'disk_test.db')

    sqlite3.connect(path)

    db = faro.Database.from_sqlite(path)

    table = faro.Table(data)
    db.add_table(table, 'other_fruits')

    os.remove(path)

def test_import_sqlite_has_name():
    """Test loading a database from disk"""
    path = os.path.join(TEST_PATH, 'disk_test.db')

    sqlite3.connect(path)

    db = faro.Database.from_sqlite(path)

    assert db.name == 'disk_test'

    os.remove(path)

def test_import_sqlite_no_extension_has_name():
    """Test loading a database from disk"""
    path = os.path.join(TEST_PATH, 'disk_test')

    sqlite3.connect(path)

    db = faro.Database.from_sqlite(path)

    assert db.name == 'disk_test'

    os.remove(path)

def test_import_sqlite_has_path():
    """Test loading a database from disk"""
    directory = os.path.join(TEST_PATH, 'test')
    os.makedirs(directory, exist_ok=True)

    path = os.path.join(directory, 'disk_test.db')

    sqlite3.connect(path)

    db = faro.Database.from_sqlite(path)

    assert db.name == 'disk_test'

    os.remove(path)
    os.rmdir(directory)
