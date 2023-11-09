import streamlit as st

from logics import Dataset

def display_tab_df_content(file_path):
    # Instantiate the Dataset class and set the data
    dataset = Dataset(file_path)
    dataset.set_df() 
    dataset.set_data() 
    dataset.set_dimensions()
    dataset.set_numeric()
    dataset.set_columns()

    # Store the dataset in st.session_state
    st.session_state['dataset'] = dataset

    st.title("DataFrame")

    # Expander for displaying dataset summary
    with st.expander("Dataframe"):
        summary_data = dataset.get_summary()
        st.table(summary_data)

    # Expander for selecting rows to display
    with st.expander("Explore Dataframe"):
        num_rows = st.slider("Select the number of rows to be displayed", 5, 50, 5)
        display_method = st.radio("Exploration Method", ("Head", "Tail", "Sample"))

        st.header("Top Rows of Selected Table")

        if display_method == "Head":
            st.dataframe(dataset.get_head(num_rows))
        elif display_method == "Tail":
            st.dataframe(dataset.get_tail(num_rows))
        else:
            st.dataframe(dataset.get_sample(num_rows))

    # Display column information
    st.header("Columns")
    st.table(dataset.table)
