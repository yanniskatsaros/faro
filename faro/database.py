import os
from pathlib import Path
from shutil import copyfile
from sqlite3 import connect
from typing import List, Callable, Iterable, Optional, Union

from pandas import (  # type: ignore
    DataFrame, read_csv,
    read_json, read_excel
)

from .table import Table

FARO_SESSION_PATH = Path('.faro.db').resolve()

class Database:
    def __init__(self, name: str, connection: Optional[Union[str, Path]]=None):
        if not connection:
            # creates a hidden file for the session
            self._session_path = FARO_SESSION_PATH
            connection = FARO_SESSION_PATH

        self._session_path = connection
        self._conn = connect(connection)
        self._cursor = self._conn.cursor()
        self._name = str(name)
        self._tables: List[str] = []
        self.table = TableProperties(self)

    def __del__(self):
        self._cursor.close()
        self._conn.close()
        del self._cursor, self._conn

        # cleanup the session files only if we created them
        if os.path.exists(FARO_SESSION_PATH):
            os.remove(FARO_SESSION_PATH)

    def __repr__(self):
        return f'Database("{self._name}")'

    @classmethod
    def from_sqlite(cls, connection: str):
        basename = os.path.basename(connection)
        name, _ = os.path.splitext(basename)
        return cls(name, connection=connection)

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

    def _parse_file(self, file: str, name: str, if_exists: str, *args, **kwargs):
        if not os.path.exists(file):
            raise FileNotFoundError(file)

        # split file name and extension
        _, file_ext = os.path.splitext(file)

        funcs = {
            '.csv': read_csv,
            '.json': read_json,
            '.xlsx': read_excel
        }

        if file_ext not in funcs.keys():
            msg = f"""Extension: {file_ext} not supported!
            Supported extensions: {funcs.keys()}
            """
            raise TypeError(msg)

        # dispatch the function based upon the extension
        read_func = funcs[file_ext]
        df = read_func(file, *args, **kwargs)
        self._parse_dataframe(df, name, if_exists)

    def _parse_faro_table(self, table: Table, name: str, if_exists: str):
        self._parse_dataframe(table.to_dataframe(), name, if_exists)

    def _parse_dataframe(self, df: DataFrame, name: str, if_exists: str):
        df.to_sql(name, self._conn, if_exists=if_exists, index=False)

    def to_sqlite(self, name=None) -> None:
        """
        Saves the database inclduing all tables, data, and
        metadata as a SQLite flat file.

        Parameters
        ----------
        name : str, optional, default `{self.name}.db`
            The name of the database. Default is
            `{self.name}.db`

        """
        if name:
            DB_NAME = name
        else:
            DB_NAME = f'{self._name}.db'

        # simply copy the flat file from the session to the dest
        DB_PATH = Path(DB_NAME).resolve()
        copyfile(self._session_path, DB_PATH)
        
    def query(self, sql: str):
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

    def map(self,
            func: Callable,
            table: str,
            columns: Iterable[str],
            output: str,
            overwrite=False) -> None:
        """
        Maps a function across each row for the
        given set of columns and stores the result
        as a new column in the given table.

        Parameters
        ----------
        func : Callable
            The function (callable) to map

        table : str
            The name of the table containing the columns

        columns : Iterable[str]
            The column(s) to map the function across

        output : str
            The name of the new column to save the result

        overwrite : bool, default False
            Overwrite the rows of the output column if it already exists
            - `True` : overwrites each row in the output column, if it already exists
            - `False` : raises `ValueError`

        Raises
        ------
        `ValueError`
            When `overwrite=False` and the output column already exists

        """
        if not isinstance(func, Callable):  # type: ignore
            raise TypeError(f'{func.__name__} is not callable')
        if not isinstance(table, str):
            raise TypeError('`table` must be of type str')
        if not isinstance(output, str):
            raise TypeError('`output` must be of type str')
        try:
            columns = [str(c) for c in columns]
        except:
            raise TypeError('`columns` must be of type Iterable[str]')

        sql = f'SELECT * FROM {table}'
        # use DataFrame for better auto-type detection and NaN coercion
        df: DataFrame = self.query(sql).to_dataframe()

        # add new column and save result to it
        if (output in df.columns) and (overwrite == False):
            msg = f"""Column already exists: {output}.
            Set `overwrite = True` to overwrite all values in this column."""
            raise ValueError(msg)

        # each column is an argument passed into the func
        result: list = [func(*row) for row in df[columns].values]
        df[output] = result
        self.add_table(df, name=table, if_exists='replace')

        return None

    @property
    def name(self):
        """The name of the database"""
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def tables(self):
        """The names of all tables in the database"""
        return self._tables


class TableProperties:
    """
    An class to access Tables as properties.
    """
    def __init__(self, database: Database):
        self.__dict__['db'] = database

    def __getattr__(self, name):
        if name in self.db._tables:
            return self.db.query(f'SELECT * FROM {name}').to_dataframe()
        else:
            raise AttributeError(f'Table `{name}` does not exist in the database')

    def __setattr__(self, name, value):
        self.db.add_table(value, name=name, if_exists='replace')
