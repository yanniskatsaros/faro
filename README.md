<p align="left">
  <img width=50% src="docs/faro.png">
</p>

# Overview
`faro` is a wrapper for the Python SQLite API, and aims to be a SQL-driven data analysis library for Python. It is intended to complement the existing data analysis packages in the Python eco-system, such as `numpy` and `pandas`. With `faro` you can use pure SQL to work with a collection of table objects in memory and easily interoperate with `numpy` and `pandas` when needed. Lastly, `faro` plays nicely with `IPython` so you can easily interact and explore your query results.

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
