from typing import List, Tuple

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
                raise te('Column names must be an iterable.')

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
        from pandas import DataFrame
        return DataFrame(self.to_dict())
