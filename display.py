import streamlit as st
from tab_num.logics import NumericColumn
import pandas as pd

def display_tab_num_content(file_path=None, df=None):
    # Check if a file path is provided and load the dataframe if it's not already provided
    if file_path is not None and df is None:
        df = pd.read_csv(file_path)

    # Check if the dataframe is loaded
    if df is not None:
        # Create an instance of NumericColumn class
        num_col = NumericColumn(df=df)

        # Find the numeric columns in the dataframe
        num_col.find_num_cols()

        # Display a select box with the list of numeric columns found
        selected_col = st.selectbox("Select a Numeric Column", num_col.cols_list)

        # Once the user selects a column, compute all the information to be displayed
        if selected_col:
            num_col.set_data(selected_col)

            # Display an expander with the summary table
            with st.expander("Summary", expanded=True):
                summary_df = num_col.get_summary()
                st.table(summary_df)

            # Display a histogram chart of the selected numeric column
            with st.expander("Histogram", expanded=True):
                st.altair_chart(num_col.histogram, use_container_width=True)

            # Display the most frequent values in the selected numeric column
            with st.expander("Most Frequent Values", expanded=True):
                st.write(num_col.frequent)

    else:
        # If no dataframe is loaded, display an error message
        st.error("No DataFrame loaded. Please provide a file path or a DataFrame.")
