import pandas as pd


class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None

    def set_data(self):
        self.set_df()
        self.set_columns()
        self.set_dimensions()
        self.set_duplicates()
        self.set_missing()
        self.set_numeric()
        self.set_text()
        self.set_table()

# Class method that will load the uploaded CSV file as Pandas DataFrame and store it as attribute (self.df) if it hasn't been provided before.

    def set_df(self):
        if self.df is None:
            self.df = pd.read_csv(self.file_path)    


# Class method that checks if self.df is empty or none

    def is_df_none(self):
        return self.df is None  

# Class method that extract the list of columns names and store the results in the relevant attribute (self.cols_list) if self.df is not empty nor None 

    def set_columns(self):
        if not self.is_df_none():
            self.cols_list = list(self.df.columns)    

# Class method that computes the dimensions (number of columns and rows) of self.df  and store the results in the relevant attributes (self.n_rows, self.n_cols) if self.df is not empty nor None 
    def set_dimensions(self):
        if not self.is_df_none():
            self.n_rows, self.n_cols = self.df.shape 
#  Class method that computes the number of duplicated of self.df and store the results in the relevant attribute (self.n_duplicates) if self.df is not empty nor None   

    def set_duplicates(self):
        if not self.is_df_none():
            self.n_duplicates = len(self.df) - len(self.df.drop_duplicates())

# Class method that computes the number of missing values of self.df and store the results in the relevant attribute (self.n_missing) if self.df is not empty nor None 

    def set_missing(self):
        if not self.is_df_none():
            self.n_missing = self.df.isnull().sum().sum()

# Class method that computes the number of columns that are numeric type and store the results in the relevant attribute (self.n_num_cols) if self.df is not empty nor None 

    def set_numeric(self):
        if not self.is_df_none():
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            self.n_num_cols = len(numeric_cols)

# Class method that computes the number of columns that are text type and store the results in the relevant attribute (self.n_text_cols) if self.df is not empty nor None 

    def set_text(self):
        if not self.is_df_none():
            text_cols = self.df.select_dtypes(include=['object']).columns
            self.n_text_cols = len(text_cols)

# Class method that computes the first rows of self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None

    def get_head(self, n=5):
        if not self.is_df_none():
            return self.df.head(n)

# Class method that computes the last rows of self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None

    def get_tail(self, n=5):
        if not self.is_df_none():
            return self.df.tail(n)
# Class method that computes a random sample of rows of self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None

    def get_sample(self, n=5):
        if not self.is_df_none():
            return self.df.sample(n)

# Class method that computes the Dataframe containing the list of columns with their data types and memory usage and store the results in the relevant attribute (self.table) if self.df is not empty nor None
    
    def set_table(self):
        if not self.is_df_none():
          self.table = pd.DataFrame({'column': self.cols_list})
          self.table['data_type'] = self.df.dtypes.values

        # Calculate memory usage for each column
          memory_usage = []
          for column in self.cols_list:
             mem = self.df[column].memory_usage(deep=True, index=False) / (1024 * 1024)  # Calculate memory usage in MB
             memory_usage.append(f"{mem:.2f} MB")  # Format memory usage to display as "X.XX MB"

          self.table['memory'] = memory_usage


# Class method that formats all requested information from self.df to be displayed in the Dataframe tab of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

    def get_summary(self):
        summary_data = {
            'Description': ['Number of Rows', 'Number of Columns', 'Number of Duplicated Rows',
                            'Number of Rows with Missing Values', 'Number of Numeric Columns',
                            'Number of Text Columns'],
            'Value': [self.n_rows, self.n_cols, self.n_duplicates, self.n_missing,
                      self.n_num_cols, self.n_text_cols]
        }
        return pd.DataFrame(summary_data, columns=['Description', 'Value'])

