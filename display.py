import altair as alt
import matplotlib.pyplot as plt
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

    if df is None:
        st.error("No data source provided.")
        return

    date_col = DateColumn(df=df)

    date_col.find_date_cols()

    if not date_col.cols_list:
        st.error("No datetime columns found.")
        return

    selected_column = st.selectbox("Select a datetime column:", date_col.cols_list)

    if selected_column:
        date_col.set_data(selected_column)
        st.write(f"Number of Unique Values: {date_col.set_unique()}")
        st.write(f"Number of Rows with Missing Values: {date_col.set_missing()}")
        st.write(f"Number of Weekend Dates: {date_col.set_weekend()}")
        st.write(f"Number of Weekday Dates: {date_col.set_weekday()}")
        st.write(f"Number of Dates in Future: {date_col.set_future()}")
        st.write(f"Number of Rows of 1900-01-01: {date_col.set_empty_1900()}")
        st.write(f"Number of Rows of 1970-01-01: {date_col.set_empty_1970()}")
        st.write(f"Minimum Value: {date_col.set_min()}")
        st.write(f"Maximum Value: {date_col.set_max()}")

        st.write("Summary of the selected datetime column:")
        # Meet bugs use get_summary
        st.table(date_col.get_summary())

        st.write("Histogram of the selected datetime column:")
        # st.altair_chart(date_col.histogram(selected_column), use_container_width=True)

        # chart = date_col.set_barchart()
        #
        # # 显示 barchart
        # if date_col.barchart is not None:
        #     st.altair_chart(chart)
        date_col.set_barchart()

        # 显示 barchart
        # if date_col.barchart is not None:
        #     st.altair_chart(date_col.barchart)


        date_col.set_barchart()
        # if date_col.barchart:
        #     st.altair_chart(date_col.barchart, use_container_width=True)

        st.header("Top 20 Most Frequent Values:")
        top_frequent_values = date_col.set_frequent(20)
        st.dataframe(top_frequent_values)




