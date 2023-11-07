import altair as alt

import streamlit as st
import pandas as pd
from tab_date.logics import DateColumn


def display_tab_date_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_date_content (function): Function that will instantiate tab_date.logics.DateColumn class, save it into Streamlit session state and call its tab_date.logics.DateColumn.find_date_cols() method in order to find all datetime columns.
    Then it will display a Streamlit select box with the list of datetime columns found.
    Once the user select a datetime column from the select box, it will call the tab_date.logics.DateColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_date.logics.DateColumn.get_summary() as a Streamlit Table
    - the graph from tab_date.logics.DateColumn.histogram using Streamlit.altair_chart()
    - the results of tab_date.logics.DateColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """

    st.title("CSV Explorer")
    date_col = DateColumn(file_path)
    # print(file_path)
    # Find datetime columns
    date_col.find_date_cols()
    # print("-")
    # print("---")
    # print(file_path)
    # print("---=--")

    if not date_col.cols_list:
        st.error("No datetime columns found.")
        return
    date_col = DateColumn(df=df)

    # If file_path is not provided, check if df is None
    if file_path is not None and df is None:
        date_col.file_path = file_path
        # Call find_date_cols to find datetime columns

        date_col.find_date_cols()

    if not date_col.cols_list:
        st.error("No datetime columns found.")
        return
    #
    # # Display select box for datetime columns
    # selected_col = st.selectbox("Select a datetime column:", date_col.cols_list)

    # Set data for the selected column
    # date_col.set_data(selected_col)
    #
    # # Create an expander container for displaying the results
    # with st.expander("Date Column Information"):
    #     # Display the summary as a table
    #     st.write("Summary of the selected datetime column:")
    #     st.table(date_col.get_summary())
    #
    #     # Display the histogram using altair_chart
    #     st.write("Histogram of the selected datetime column:")
    #     st.altair_chart(date_col.histogram(), use_container_width=True)
    #
    #     # Display the frequent values
    #     st.write("Frequent values in the selected datetime column:")
    #     st.write(date_col.frequent)
