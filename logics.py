import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(uploaded_file):
    # Assuming the file is a CSV
    return pd.read_csv(uploaded_file)

def get_numeric_columns(df):
    return df.select_dtypes(include=np.number).columns.tolist()

def get_descriptive_stats(df, numeric_column):
    return df[numeric_column].describe()

def get_histogram(df, numeric_column):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[numeric_column], kde=True)
    plt.title(f'Histogram of {numeric_column}')
    plt.xlabel(numeric_column)
    plt.ylabel('Count')
    plt.grid(True)
    plt.tight_layout()
    return plt

def get_boxplot(df, numeric_column):
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df[numeric_column])
    plt.title(f'Boxplot of {numeric_column}')
    plt.ylabel(numeric_column)
    plt.grid(True)
    plt.tight_layout()
    return plt
