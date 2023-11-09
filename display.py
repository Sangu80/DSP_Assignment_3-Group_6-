import streamlit as st
from .logics import load_data, get_numeric_columns, get_descriptive_stats, get_histogram, get_boxplot

def show_numeric_tab(uploaded_file):
    df = load_data(uploaded_file)
    numeric_columns = get_numeric_columns(df)
    
    st.subheader('Numeric Data Analysis')
    numeric_column = st.selectbox('Select the Numeric Column', numeric_columns)
    if numeric_column:
        st.write('Descriptive Statistics')
        st.table(get_descriptive_stats(df, numeric_column))

        st.write('Histogram')
        hist_fig = get_histogram(df, numeric_column)
        st.pyplot(hist_fig)

        st.write('Boxplot')
        box_fig = get_boxplot(df, numeric_column)
        st.pyplot(box_fig)
