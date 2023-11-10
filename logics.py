# tab_text/logics.py

import pandas as pd
import altair as alt

class TextColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty  = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_text_cols(self):
        if self.df is None and self.file_path is not None:
            self.df = pd.read_csv(self.file_path)

        if self.df is not None:
            self.cols_list = [col for col in self.df.columns if self.df[col].dtype == 'object']

    def set_data(self, col_name):
        self.serie = self.df[col_name] if col_name in self.df.columns else None
        if self.is_serie_none():
            return

        self.convert_serie_to_text()
        self.set_unique()
        self.set_missing()
        self.set_empty()
        self.set_mode()
        self.set_whitespace()
        self.set_lowercase()
        self.set_uppercase()
        self.set_alphabet()
        self.set_digit()
        self.set_barchart()
        self.set_frequent()

    def convert_serie_to_text(self):
        self.serie = self.serie.astype(str)

    def is_serie_none(self):
        return self.serie is None or self.serie.empty

    def set_unique(self):
        self.n_unique = self.serie.nunique()

    def set_missing(self):
        self.n_missing = self.serie.isnull().sum()

    def set_empty(self):
        self.n_empty = (self.serie == '').sum()

    def set_mode(self):
        self.n_mode = self.serie.mode().iloc[0]

    def set_whitespace(self):
        self.n_space = self.serie.apply(lambda x: x.isspace()).sum()

    def set_lowercase(self):
        self.n_lower = self.serie.str.islower().sum()

    def set_uppercase(self):
        self.n_upper = self.serie.str.isupper().sum()

    def set_alphabet(self):
        self.n_alpha = self.serie.apply(lambda x: x.isalpha()).sum()

    def set_digit(self):
        self.n_digit = self.serie.apply(lambda x: x.isdigit()).sum()

    def set_barchart(self):
        chart = alt.Chart(self.serie.reset_index(), height=300).mark_bar().encode(
            x=alt.X('index:N', title='Values'),
            y=alt.Y('count()', title='Count'),
            tooltip=['index:N', 'count()']
        ).interactive()

        self.barchart = chart

    def set_frequent(self, end=20):
        value_counts = self.serie.value_counts().head(end).reset_index()
        value_counts.columns = ['value', 'occurrence']
        value_counts['percentage'] = (value_counts['occurrence'] / len(self.serie)) * 100

        self.frequent = value_counts

    def get_summary(self):
        summary_data = [
            ("Number of Unique Values", self.n_unique),
            ("Number of Missing Values", self.n_missing),
            ("Number of Empty Values", self.n_empty),
            ("Mode Value", self.n_mode),
            ("Number of Whitespace Values", self.n_space),
            ("Number of Lowercase Values", self.n_lower),
            ("Number of Uppercase Values", self.n_upper),
            ("Number of Alphabetical Values", self.n_alpha),
            ("Number of Numeric Values", self.n_digit)
        ]

        summary_df = pd.DataFrame(summary_data, columns=['Description', 'Value'])
        return summary_df
