import os
from sqlite3 import connect

from pandas import (
    DataFrame, read_csv,
    read_json, read_excel
)

from .table import Table

class Database:
    def __init__(self, name : str):
        self._conn = connect(':memory:')
        self._cursor = self._conn.cursor()
        self._name = str(name)
        self._tables = []

    def __del__(self):
        self._cursor.close()
        self._conn.close()
        del self._cursor, self._conn

    def __repr__(self):
        return f'Database("{self._name}")'

    def add_table(self, table, name, if_exists='fail', *args, **kwargs):
        """
        Load the contents of a file, or table
        to the current database.

        Directly specify a filepath, a
        `pandas.DataFrame`, or a `faro.Table`.

        Parameters
        ----------
        table : [str, pandas.DataFrame, faro.Table]
            The table data or file name to add to the
            database.

            If a `str` is provided, it is interpreted
            as a filepath and will be parsed according
            to the file type. Current support includes:
                - csv, json, xlsx
            
            If a `pandas.DataFrame` or `faro.Table` is
            provided, it is directly parsed and added
            to the database.

        name : str
            The name the table will be stored
            under in the database.

        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            How to behave if the table already exists.
            - fail: raise a `ValueError`
            - replace: drop the existing table before adding it
            - append: insert new values to the existing table

        Raises
        ------
        `ValueError`
            When `if_exists = 'fail'` and the table already exists.

        `FileNotFoundError`
            The path to the file specified is invalid.

        """
        if if_exists not in ('fail', 'replace', 'append'):
            raise ValueError('Valid options: {"fail", "replace", "append"}')

        if name in self._tables and if_exists == 'fail':
            raise ValueError(f'Table: {name} already exists in database.')

        # handle types appropriately
        if isinstance(table, (str)):
            self._parse_file(table, name, if_exists, *args, **kwargs)
        elif isinstance(table, (Table)):
            self._parse_faro_table(table, name, if_exists)
        elif isinstance(table, (DataFrame)):
            self._parse_dataframe(table, name, if_exists)
        else:
            msg = """Invalid table type.
            Valid types include:
                - str (file name)
                - `faro.Table`
                - `pandas.DataFrame`
            """
            raise TypeError(msg)

        if name not in self._tables:
           self._tables.append(name)

    def _parse_file(self, file : str, name : str, if_exists : str, *args, **kwargs):
        if not os.path.exists(file):
            raise FileNotFoundError(file)

        # split file name and extension
        _, file_ext = os.path.splitext(file)

        funcs = {
            '.csv' : read_csv,
            '.json' : read_json,
            '.xlsx' : read_excel
        }

        if file_ext not in funcs.keys():
            msg = f"""Extension: {file_ext} not supported!
            Supported extensions: {funcs.keys()}
            """
            raise TypeError(msg)

        # dispatch the function based upon the extension
        read_func = funcs.get(file_ext)
        df = read_func(file, *args, **kwargs)
        self._parse_dataframe(df, name, if_exists)

    def _parse_faro_table(self, table : Table, name : str, if_exists : str):
        self._parse_dataframe(table.to_dataframe(), name, if_exists)

    def _parse_dataframe(self, df : DataFrame, name : str, if_exists : str):
        df.to_sql(name, self._conn, if_exists=if_exists, index=False)

    def to_sqlite(self, name=None):
        """
        Saves the database inclduing all tables, data, and
        metadata as a SQLite flat file.

        Parameters
        ----------
        name : str, optional, default `{name}.db`
            The name of the database. Default is
            the {object instance name}.db

        """
        if name:
            DB_NAME = name
        else:
            DB_NAME = f'{self._name}.db'

        with connect(DB_NAME) as bck:
            self._conn.backup(bck)
        

    def query(self, sql : str):
        """
        Executes the specified SQL statement
        against the database and returns the
        result set as a `faro.Table`.
        
        This method is useful for executing
        "read" statements against the database 
        that return rows of data. For operations
        such as manually creating tables or
        inserting data into tables, use
        `faro.Database.execute` instead.

        Parameters
        ----------
        sql : str
            The SQL query to execute

        Returns
        -------
        `faro.Table`

        See Also
        --------
        faro.Database.execute : Executes an arbitrary SQL
            statement against the database.
        """
        # check that a single statement was passed
        expressions = [e for e in sql.split(';') if e != '']
        if len(expressions) > 1:
            raise ValueError('Can only execute a single statement at once.')

        self._cursor.execute(sql)
        return Table(
            self._cursor.fetchall(),
            header=False,
            columns=[row[0] for row in self._cursor.description]
        )

    @property
    def name(self):
        """The name of the database"""
        return self._name

    @name.setter
    def name(self, name : str):
        self._name = name

    @property
    def tables(self):
        """The names of all tables in the database"""
        return self._tables
    