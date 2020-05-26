# setup.py automatically generated using poetry
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faro']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0', 'pydantic>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'faro',
    'version': '0.0.4',
    'description': 'An SQL-focused data analysis library for Python',
    'long_description': '<p align="left">\n  <img width=40% src="https://raw.githubusercontent.com/yanniskatsaros/faro/master/docs/faro.svg?sanitize=true">\n</p>\n\n![PyPI - License](https://img.shields.io/pypi/l/faro)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faro)\n![PyPI](https://img.shields.io/pypi/v/faro?color=blue)\n[![Build Status](https://travis-ci.com/yanniskatsaros/faro.svg?branch=master)](https://travis-ci.com/yanniskatsaros/faro)\n\n# Overview\n`faro` is a fast, simple, and intuitive SQL-driven data analysis library for Python. It is built on top of `sqlite` and is intended to complement the existing data analysis packages in the Python eco-system, such as `numpy`, `pandas`, and `matplotlib` by providing easy interoperability between them. It also integrates with Jupyter by default to provide readable and interactive displays of queries and tables.\n\n# Usage\nCreate a `Database` object and give it a name.\n```python\nfrom faro import Database\n\ndb = Database(\'transportation\')\n```\n\nTo add tables to the in-memory database, simply specify the name of the file. Supported file types include: `csv`, `json`, and `xlsx`. `add_table` inserts the contents of a file into a new table within the database. It can automatically detect the filetype and parse the file contents accordingly. In this example we load two different tables, one in `csv` format, and the other in `json` format.\n```python\ndb.add_table(\'cars.json\', name=\'cars\')\ndb.add_table(\'airports.csv\', name=\'airports\')\n```\n\nWe can also directly pass `pandas.DataFrame` or `faro.Table` objects to be added to the database. A helpful pattern when dealing with more complex parsing for a specific file is to read it into memory using `pandas` then add the `DataFrame` to the `faro.Database`.\n```python\nbuses = pd.DataFrame({\n  \'id\' : [1, 2, 3, 4, 5],\n  \'from\' : [\'Houston\', \'Atlanta\', \'Chicago\', \'Boston\', \'New York\'],\n  \'to\' : [\'San Antonio\', \'Charlotte\', \'Milwaukee\', \'Cape Cod\', \'Buffalo\']\n})\n\ndb.add_table(buses, name=\'buses\')\n```\n\nAlternatively, we can directly assign to a table name as a property of the `table` object. Using this method, however, will also replace the entire table as opposed to the options offered by `add_table()`\n```python\ndb.table.buses = buses\n```\n\nWe can now query against any table in the database using pure SQL, and easily interact with the results in a Jupyter Notebook.\n```python\nsql = """\nSELECT iata,\n       name,\n       city,\n       state\n  FROM airports\n WHERE country = \'USA\'\n LIMIT 5\n"""\ndb.query(sql)\n```\n<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>iata</th>\n      <th>name</th>\n      <th>city</th>\n      <th>state</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>00M</td>\n      <td>Thigpen</td>\n      <td>Bay Springs</td>\n      <td>MS</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>00R</td>\n      <td>Livingston Municipal</td>\n      <td>Livingston</td>\n      <td>TX</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>00V</td>\n      <td>Meadow Lake</td>\n      <td>Colorado Springs</td>\n      <td>CO</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>01G</td>\n      <td>Perry-Warsaw</td>\n      <td>Perry</td>\n      <td>NY</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>01J</td>\n      <td>Hilliard Airpark</td>\n      <td>Hilliard</td>\n      <td>FL</td>\n    </tr>\n  </tbody>\n</table>\n\nIf we want to interact with the data returned by the query, we can easily transform it into whatever data type is most convenient for the situation. Supported type conversions include: `List[Tuple]`, `Dict[List]`, `numpy.ndarray`, and `pandas.DataFrame`.\n\n```python\ntable = db.query(sql)\ntype(table)\n>>> faro.table.Table\n\ndf = table.to_dataframe()\ntype(df)\n>>> pandas.core.frame.DataFrame\n\nmatrix = table.to_numpy()\ntype(matrix)\n>>> numpy.ndarray\n```\n\nWe can also interact with the tables in our database by accessing them as properties of the `table` object. For example:\n\n```python\ndb.table.buses\n```\n<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>id</th>\n      <th>from</th>\n      <th>to</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>1</th>\n      <td>1</td>\n      <td>Houston</td>\n      <td>San Antonio</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2</td>\n      <td>Atlanta</td>\n      <td>Charlotte</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <th>3</th>\n      <td>Chicago</td>\n      <td>Milwaukee</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <th>4</th>\n      <td>Boston</td>\n      <td>Cape Cod</td>\n    </tr>\n    <tr>\n      <th>5</th>\n      <th>5</th>\n      <td>New York</td>\n      <td>Buffalo</td>\n    </tr>\n  </tbody>\n</table>\n',
    'author': 'Yannis Katsaros',
    'author_email': 'yanniskatsaros@hotmail.com',
    'maintainer': 'Yannis Katsaros',
    'maintainer_email': 'yanniskatsaros@hotmail.com',
    'url': 'https://github.com/yanniskatsaros/faro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
