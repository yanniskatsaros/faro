import inspect
from datetime import date, datetime
from typing import List, Tuple, Type, Type, Optional

from pydantic import create_model
from pydantic.fields import ModelField

# see https://www.sqlite.org/datatype3.html
# 3.1.1 Affinity Name Examples
SQLITE_TYPEMAP = {
    str: 'TEXT',
    float: 'REAL',
    int: 'INTEGER',
    date: 'DATE',
    datetime: 'DATETIME',
    bool: 'NUMERIC',
    None: 'BLOB',
}

class Table:
    def __init__(self, data : List[Tuple], header=True, columns=None):
        self.n_rows = len(data)
        self.n_cols = len(data[0])
        self.shape = (self.n_rows, self.n_cols)

        # uses the column names from the first row of the data
        if header:
            self.columns = [str(c) for c in data[0]]
            self.data = [tuple(row) for row in data[1:]]
        else:
            self.columns = [str(i) for i in range(self.n_cols)]
            self.data = [tuple(row) for row in data]

        # overrides the column names
        if columns:
            try:
                self.columns = list(columns)
            except TypeError as te:
                raise te('Column names must be an iterable.')  # type: ignore

    def _repr_html_(self):
        """
        Return an HTML representation for the given table.

        Intended for use with IPython notebook.
        """
        return self.to_dataframe()._repr_html_()

    def to_list(self):
        """
        Returns the data represented as a
        list of tuples.
        """
        return self.data

    def to_numpy(self):
        """
        Returns the data represented as a
        NumPy matrix of type: `numpy.ndarray`
        and shape (m, n).
        """
        return self.to_dataframe().to_numpy()

    def to_dict(self):
        """
        Returns the data represented as
        a dictionary where each key
        represents each column, and each
        value is an array of the column data.
        """
        out = {}
        for i, col in enumerate(self.columns):
            out[col] = [row[i] for row in self.data]

        return out

    def to_dataframe(self):
        """
        Returns the data represented as
        a `pandas.DataFrame`
        """
        from pandas import DataFrame  # type: ignore
        return DataFrame(self.to_dict())

def table(cls: Type, name: Optional[str]=None):
    """
    `dataclass` style decorator for easily defining
    table schema using type hints and default values.

    Parameters
    ----------
    cls: Type
        The class definition to decorate

    name: Optional[str] = None
        Optionally override the default name of the
        decorated class name. If `None` is provided
        it will use `cls.__name__.lower()` for the
        name of the table in the schema.

    Returns
    -------
    cls

    """
    if not inspect.isclass(cls):
        got_type = type(cls)
        raise TypeError(f'Expected input type: class, got: {got_type}')

    # TODO - refer back to https://github.com/samuelcolvin/pydantic/issues/153#issuecomment-633708838
    # clean attribute names with trailing underscore such as `from_` or `int_` for
    # any fields that clash with Python keywords
    # potentially use a `normalize: Optional[bool] = False` kwarg to handle this behavior?

    ann: dict = cls.__annotations__
    cls_map: dict = cls.__dict__
    signature = {a: (t, cls_map.get(a, ...)) for a, t in ann.items()}

    cls = create_model(cls.__name__, **signature)

    # use the input class name for the underlying table name
    if not name:
        name: str = cls.__name__.lower()

    def sql_schema() -> str:
        """
        Generates a SQLite3 compatible table schema
        that can be used to create a table in a database.

        Returns
        -------
        sql: str
            Table schema definition

        """
        # FIXME fails if the default values provided is `None`
        def field_to_column(f: ModelField) -> str:
            REQUIRED = {
                True: 'NOT NULL',
                False: f'DEFAULT {f.default}'
            }
            return f'{f.name} {SQLITE_TYPEMAP[f.type_]} {REQUIRED[f.required]}'
        
        column_defs = [field_to_column(f) for f in cls.__fields__.values()]
        schema = ',\n'.join('    ' + cdf for cdf in column_defs)

        return f'CREATE TABLE IF NOT EXISTS {name} (\n{schema}\n)'    

    def sql_insert() -> str:
        """
        Generates a SQLite3 compatible SQL insert statement
        using the model fields and types.

        Returns
        -------
        sql: str
            Insert statement
        
        """
        cols: str = ', '.join(f.name for f in cls.__fields__.values())
        wildcards: str = ', '.join('?' for _ in range(len(cls.__fields__)))
        
        return f'INSERT INTO {name}({cols}) VALUES ({wildcards})'

    def sql_drop() -> str:
        return f'DROP TABLE IF EXISTS {name}'

    return type(
        cls.__name__,
        (cls, ),
        {
            'columns': lambda: list(cls.__fields__.keys()),
            'sql_schema': sql_schema,
            'sql_insert': sql_insert,
            'sql_drop': sql_drop,
        }
    )
