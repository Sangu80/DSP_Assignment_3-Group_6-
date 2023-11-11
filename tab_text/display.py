# tab_text/display.py
import streamlit as st
from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None,df=None):
    st.title("Text Serie Analysis")

    text_column_instance = TextColumn(file_path, df)
    text_column_instance.find_text_cols()

    if not text_column_instance.cols_list:
        st.warning("No text columns found in the dataset.")
        return

    selected_column = st.selectbox("Select a text column to explore:", text_column_instance.cols_list)
    text_column_instance.set_data(selected_column)

    with st.expander("Text Column Analysis"):
        st.subheader("Summary:")
        st.table(text_column_instance.get_summary())

        st.subheader("Histogram:")
        st.altair_chart(text_column_instance.barchart)

        st.subheader("Top 20 Most Frequent Values:")
        st.dataframe(text_column_instance.frequent)
