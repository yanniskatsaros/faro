<p align="left">
  <img width=40% src="https://raw.githubusercontent.com/yanniskatsaros/faro/master/docs/faro.svg?sanitize=true">
</p>

![PyPI - License](https://img.shields.io/pypi/l/faro)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faro)
![PyPI](https://img.shields.io/pypi/v/faro?color=blue)
[![Build Status](https://travis-ci.com/yanniskatsaros/faro.svg?branch=master)](https://travis-ci.com/yanniskatsaros/faro)

# Overview
`faro` is a fast, simple, and intuitive SQL-driven data analysis library for Python. It is built on top of `sqlite` and is intended to complement the existing data analysis packages in the Python eco-system, such as `numpy`, `pandas`, and `matplotlib` by providing easy interoperability between them. It also integrates with Jupyter by default to provide readable and interactive displays of queries and tables.

# Usage
Create a `Database` object and give it a name.
```python
from faro import Database

db = Database('transportation')
```

To add tables to the in-memory database, simply specify the name of the file. Supported file types include: `csv`, `json`, and `xlsx`. `add_table` inserts the contents of a file into a new table within the database. It can automatically detect the filetype and parse the file contents accordingly. In this example we load two different tables, one in `csv` format, and the other in `json` format.
```python
db.add_table('cars.json', name='cars')
db.add_table('airports.csv', name='airports')
```

We can also directly pass `pandas.DataFrame` or `faro.Table` objects to be added to the database. A helpful pattern when dealing with more complex parsing for a specific file is to read it into memory using `pandas` then add the `DataFrame` to the `faro.Database`.
```python
buses = pd.DataFrame({
  'id' : [1, 2, 3, 4, 5],
  'from' : ['Houston', 'Atlanta', 'Chicago', 'Boston', 'New York'],
  'to' : ['San Antonio', 'Charlotte', 'Milwaukee', 'Cape Cod', 'Buffalo']
})

db.add_table(buses, name='buses')
```

Alternatively, we can directly assign to a table name as a property of the `table` object. Using this method, however, will also replace the entire table as opposed to the options offered by `add_table()`
```python
db.table.buses = buses
```

We can now query against any table in the database using pure SQL, and easily interact with the results in a Jupyter Notebook.
```python
sql = """
SELECT iata,
       name,
       city,
       state
  FROM airports
 WHERE country = 'USA'
 LIMIT 5
"""
db.query(sql)
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>iata</th>
      <th>name</th>
      <th>city</th>
      <th>state</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>00M</td>
      <td>Thigpen</td>
      <td>Bay Springs</td>
      <td>MS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>00R</td>
      <td>Livingston Municipal</td>
      <td>Livingston</td>
      <td>TX</td>
    </tr>
    <tr>
      <th>2</th>
      <td>00V</td>
      <td>Meadow Lake</td>
      <td>Colorado Springs</td>
      <td>CO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>01G</td>
      <td>Perry-Warsaw</td>
      <td>Perry</td>
      <td>NY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>01J</td>
      <td>Hilliard Airpark</td>
      <td>Hilliard</td>
      <td>FL</td>
    </tr>
  </tbody>
</table>

If we want to interact with the data returned by the query, we can easily transform it into whatever data type is most convenient for the situation. Supported type conversions include: `List[Tuple]`, `Dict[List]`, `numpy.ndarray`, and `pandas.DataFrame`.

```python
table = db.query(sql)
type(table)
>>> faro.table.Table

df = table.to_dataframe()
type(df)
>>> pandas.core.frame.DataFrame

matrix = table.to_numpy()
type(matrix)
>>> numpy.ndarray
```

We can also interact with the tables in our database by accessing them as properties of the `table` object. For example:

```python
db.table.buses
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>from</th>
      <th>to</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Houston</td>
      <td>San Antonio</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Atlanta</td>
      <td>Charlotte</td>
    </tr>
    <tr>
      <th>3</th>
      <th>3</th>
      <td>Chicago</td>
      <td>Milwaukee</td>
    </tr>
    <tr>
      <th>4</th>
      <th>4</th>
      <td>Boston</td>
      <td>Cape Cod</td>
    </tr>
    <tr>
      <th>5</th>
      <th>5</th>
      <td>New York</td>
      <td>Buffalo</td>
    </tr>
  </tbody>
</table>
