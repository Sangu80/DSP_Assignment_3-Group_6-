
import streamlit as st
from logics import Dataset


def display_tab_df_content(file_path):
    # Instantiate the Dataset class and set the data
    dataset = Dataset(file_path)
    dataset.set_data()

    st.title("Data Analysis - DataFrame")

    # Expander for displaying dataset summary
    with st.expander("Dataset Summary"):
        summary_data = dataset.get_summary()
        st.table(summary_data)

    # Expander for selecting rows to display
    with st.expander("Select Rows to Display"):
        num_rows = st.slider("Select the number of rows to display", 5, 50, 5)
        display_method = st.radio("Select the display method", ("head", "tail", "sample"))

        if display_method == "head":
            st.dataframe(dataset.get_head(num_rows))
        elif display_method == "tail":
            st.dataframe(dataset.get_tail(num_rows))
        else:
            st.dataframe(dataset.get_sample(num_rows))

    # Display column information
    st.header("Column Information")
    st.table(dataset.table)

