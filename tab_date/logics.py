import datetime

import pandas as pd
import altair as alt
import streamlit as st

class DateColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])



    def find_date_cols(self):
        if self.df is not None:
            date_cols = [col for col in self.df.columns if pd.api.types.is_datetime64_any_dtype(self.df[col])]
            if date_cols:
                self.cols_list = date_cols
            else:
                # If no datetime columns are found, look for text columns
                text_cols = [col for col in self.df.columns if pd.api.types.is_string_dtype(self.df[col])]
                self.cols_list = text_cols
        else:
            st.error("DataFrame is not loaded. Please load a DataFrame first.")


    def set_data(self, col_name):
        if self.df is not None:
            if col_name in self.df.columns:
                self.serie = self.df[col_name]
                self.convert_serie_to_date()
                self.set_unique()
                self.set_missing()
                self.set_min()
                self.set_max()
                self.set_weekend()
                self.set_weekday()
                self.set_future()
                self.set_empty_1900()
                self.set_empty_1970()
                self.set_barchart()
                self.set_frequent()

    def convert_serie_to_date(self):
        if not self.is_serie_none():
            self.serie = pd.to_datetime(self.serie,dayfirst=True)


    def is_serie_none(self):
        return self.serie is None

    def set_unique(self):
        if not self.is_serie_none():
            self.n_unique = len(self.serie.unique())
            return self.n_unique

    def set_missing(self):
        if not self.is_serie_none():
            self.n_missing = self.serie.isna().sum()
            return self.n_missing

    def set_min(self):
        if not self.is_serie_none():
            self.col_min = self.serie.min()
            return self.col_min

    def set_max(self):
        if not self.is_serie_none():
            self.col_max = self.serie.max()
            return self.col_max

    def set_weekend(self):
        if not self.is_serie_none():
            self.n_weekend = len([d for d in self.serie if d.weekday() > 5])
            return self.n_weekend

    def set_weekday(self):
        if not self.is_serie_none():
            self.n_weekday = len([d for d in self.serie if d.weekday() <= 5])
            return self.n_weekday

    def set_future(self):
        if not self.is_serie_none():
            today = datetime.datetime.now()
            self.n_future = len([d for d in self.serie if d > today])
            return self.n_future

    def set_empty_1900(self):
        if not self.is_serie_none():
            self.n_empty_1900 = len([d for d in self.serie if d == datetime.datetime(1900, 1, 1)])
            return self.n_empty_1900

    def set_empty_1970(self):
        if not self.is_serie_none():
            self.n_empty_1970 = len([d for d in self.serie if d == datetime.datetime(1970, 1, 1)])
            return self.n_empty_1970

    def set_barchart(self):
        if not self.is_serie_none():
            #print((self.cols_list))
            chart_data = self.serie.to_frame().reset_index()

            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X(f'{self.cols_list}:T', title='Date'),
                y=alt.Y('count():Q', title='Count')
            ).properties(width = 600, height = 400).interactive()
            self.barchart = chart
            return self.barchart


    def set_frequent(self, end=20):
        if self.serie is None:
            # print("The serie is not initialized. Load a column first.")
            return

        if not isinstance(end, int) or end <= 0:
            print("Invalid 'end' parameter. It should be a positive integer.")
            return

        frequent_series = self.serie.value_counts().head(end)
        relative_frequency = frequent_series / len(self.serie)  # Calculate relative frequency
        self.frequent = pd.DataFrame({
                                      'occurrence': frequent_series.values,
                                      'percentage': relative_frequency * 100}, index=frequent_series.index).reset_index()


        return self.frequent

    def get_summary(self):
        summary = pd.DataFrame({
            'Description': ['Number of Unique Values', 'Number of Missing Values', 'Minimum Date', 'Maximum Date',
                            'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Future Dates',
                            'Number of Dates Equal to 1900-01-01', 'Number of Dates Equal to 1970-01-01'],
            'Value': [self.n_unique, self.n_missing, self.col_min, self.col_max,
                      self.n_weekend, self.n_weekday, self.n_future, self.n_empty_1900, self.n_empty_1970]
        })
        return summary


