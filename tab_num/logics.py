import pandas as pd
import altair as alt

class NumericColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = pd.read_csv(file_path) if file_path else df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_num_cols(self):
        if self.df is not None:
            numeric_cols = self.df.select_dtypes(include='number').columns
            self.cols_list = numeric_cols.tolist()

    def set_data(self, col_name):
        self.serie = self.df[col_name]
        self.convert_serie_to_num()
        if not self.is_serie_none():
            self.set_unique()
            self.set_missing()
            self.set_zeros()
            self.set_negatives()
            self.set_mean()
            self.set_std()
            self.set_min()
            self.set_max()
            self.set_median()
            self.set_histogram()
            self.set_frequent()

    def convert_serie_to_num(self):
        self.serie = pd.to_numeric(self.serie, errors='coerce')

    def is_serie_none(self):
        return self.serie is None or self.serie.empty

    def set_unique(self):
        self.n_unique = self.serie.nunique(dropna=True)

    def set_missing(self):
        self.n_missing = self.serie.isna().sum()

    def set_zeros(self):
        self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        self.n_negatives = (self.serie < 0).sum()

    def set_mean(self):
        self.col_mean = self.serie.mean()

    def set_std(self):
        self.col_std = self.serie.std()

    def set_min(self):
        self.col_min = self.serie.min()

    def set_max(self):
        self.col_max = self.serie.max()

    def set_median(self):
        self.col_median = self.serie.median()

    def set_histogram(self):
        self.histogram = alt.Chart(self.df).mark_bar().encode(
            alt.X(self.serie.name, bin=True),
            y='count()'
        )

    def set_frequent(self, end=20):
        counts = self.serie.value_counts().head(end).reset_index()
        counts.columns = ['value', 'occurrence']
        total_counts = self.serie.value_counts().sum()
        counts['percentage'] = (counts['occurrence'] / total_counts) * 100
        self.frequent = counts

    def get_summary(self):
        summary_data = {
            "Description": [
                "Number of Unique values", "Number of rows with Missing values", "Mean", "Standard Deviation value",
                "Minimum value", "Maximum value", "Median value", "number of rows with 0", "Number of rows with Negative values"
            ],
            "Value": [
                self.n_unique, self.n_missing, self.col_mean, self.col_std,
                self.col_min, self.col_max, self.col_median, self.n_zeros, self.n_negatives
            ]
        }
        return pd.DataFrame(summary_data)
