# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # Use Matplotlib for data visualization

# Streamlit page configuration
st.set_page_config(page_title="Interactive Data Explorer", layout="wide")

# Main title
st.title('Interactive Data Explorer')

# Sidebar for data source selection
st.sidebar.header('Data Source Selection')
source_type = st.sidebar.selectbox('Select the data source type:', ['CSV/Excel'])

# Initialize an empty DataFrame
df = pd.DataFrame()

# Depending on the user's choice, load the data into 'df'
if source_type == 'CSV/Excel':
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        st.write(df)  # Display the dataframe in the Streamlit app

# Tabs for Data Manipulation and Data Visualization
tab1, tab2 = st.tabs(["Data Manipulation", "Data Visualization"])

# Data Manipulation Section
with tab1:
    if not df.empty:  # Check if 'df' is not empty
        st.header('Data Manipulation')

        # Sorting
        st.subheader('Sorting')
        col_to_sort = st.selectbox('Select column to sort by:', df.columns)
        sort_order = st.radio('Sort order:', ['Ascending', 'Descending'])
        if col_to_sort:
            df = df.sort_values(by=col_to_sort, ascending=(sort_order == 'Ascending'))
            st.write(df)

        # Filtering
        st.subheader('Filtering')
        filter_column = st.selectbox('Select column to filter by:', [''] + list(df.columns))
        if filter_column:
            # Use multiselect for selecting multiple filter conditions
            unique_values = df[filter_column].unique()
            selected_values = st.multiselect('Select values to filter by:', unique_values, default=list(unique_values))
            if selected_values:
                df_filtered = df[df[filter_column].isin(selected_values)]
                st.write(df_filtered)
            else:
                st.write(df)  # Display original dataframe if no filter is applied

        # Column Transformations
        st.subheader('Column Transformations')
        old_col_name = st.selectbox('Select a column to rename:', [''] + list(df.columns))
        new_col_name = st.text_input('New column name:', '')
        if old_col_name and new_col_name:
            df.rename(columns={old_col_name: new_col_name}, inplace=True)
            st.success(f'Column renamed: {old_col_name} to {new_col_name}')
            st.write(df)

        # Data type conversion
        col_to_convert = st.selectbox('Select a column for data type conversion:', [''] + list(df.columns))
        new_type = st.selectbox('Select new data type:', ['', 'float', 'int', 'str'])
        if col_to_convert and new_type:
            try:
                df[col_to_convert] = df[col_to_convert].astype(new_type)
                st.success(f'Column {col_to_convert} converted to {new_type}')
                st.write(df)
            except Exception as e:
                st.error(f'Error converting data type: {e}')

        # Create a new column based on existing ones
        st.subheader('Create New Column')
        new_column_name = st.text_input('Name for the new column:', key='new_col_name')
        new_column_formula = st.text_input('Formula (use existing column names, e.g., col1 + col2):', key='new_col_formula')
        if new_column_name and new_column_formula:
            try:
                df.eval(f'{new_column_name} = {new_column_formula}', inplace=True)
                st.success(f'New column "{new_column_name}" added successfully.')
                st.write(df)
            except Exception as e:
                st.error(f'Error creating new column: {e}')

        # Column Removal
        st.subheader('Remove Column')
        col_to_remove = st.selectbox('Select a column to remove:', [''] + list(df.columns))
        if col_to_remove:
            if st.button(f'Remove {col_to_remove}'):
                df.drop(columns=[col_to_remove], inplace=True)
                st.success(f'Column {col_to_remove} removed successfully.')
                st.write(df)

# Data Visualization Section with Filters and Sliders
with tab2:
    if not df.empty:  # Check if 'df' is not empty
        st.header('Data Visualization')

        # User selects the type of plot they want to create
        plot_types = ['Bar plot', 'Scatter plot', 'Histogram', 'Line chart', 'Box plot']
        plot_type = st.selectbox('Select the type of plot', plot_types)

        # Additional settings based on plot type
        if plot_type:
            st.subheader('Plot Settings')

            # Data Filtering for Visualization
            st.subheader('Data Filtering for Visualization')
            filter_column_vis = st.selectbox('Select column to filter by (for visualization):', ['None'] + list(df.columns))
            if filter_column_vis != 'None':
                unique_values = df[filter_column_vis].unique()
                selected_values = st.multiselect(f'Select values from {filter_column_vis} to include in the plot:', unique_values, default=list(unique_values))
                df_filtered_vis = df[df[filter_column_vis].isin(selected_values)]
            else:
                df_filtered_vis = df

            # Plotting based on the filtered dataframe and user choices
            if plot_type == 'Bar plot':
                x_value = st.selectbox('X-axis', options=df_filtered_vis.columns)
                y_value = st.selectbox('Y-axis', options=df_filtered_vis.columns)
                fig, ax = plt.subplots()
                df_filtered_vis.groupby(x_value)[y_value].sum().plot(kind='bar', ax=ax)
                ax.set_xlabel(x_value)
                ax.set_ylabel(y_value)
                st.pyplot(fig)

            elif plot_type == 'Scatter plot':
                x_value = st.selectbox('X-axis', options=df_filtered_vis.columns)
                y_value = st.selectbox('Y-axis', options=df_filtered_vis.columns)
                fig, ax = plt.subplots()
                ax.scatter(df_filtered_vis[x_value], df_filtered_vis[y_value])
                ax.set_xlabel(x_value)
                ax.set_ylabel(y_value)
                st.pyplot(fig)

            elif plot_type == 'Histogram':
                x_value = st.selectbox('Variable for histogram:', options=df_filtered_vis.columns)
                fig, ax = plt.subplots()
                ax.hist(df_filtered_vis[x_value], bins='auto')  # 'auto' lets Matplotlib decide the number of bins
                ax.set_xlabel(x_value)
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

            elif plot_type == 'Line chart':
                x_value = st.selectbox('X-axis for line chart:', options=df_filtered_vis.columns)
                y_values = st.multiselect('Y-axis (can select multiple):', options=df_filtered_vis.columns)
                fig, ax = plt.subplots()
                for y_value in y_values:
                    ax.plot(df_filtered_vis[x_value], df_filtered_vis[y_value], label=y_value)
                ax.set_xlabel(x_value)
                ax.legend()
                st.pyplot(fig)

            elif plot_type == 'Box plot':
                y_value = st.selectbox('Variable for box plot:', options=df_filtered_vis.columns)
                fig, ax = plt.subplots()
                ax.boxplot(df_filtered_vis[y_value].dropna(), vert=False)  # 'vert=False' makes the box plot horizontal
                ax.set_xlabel(y_value)
                st.pyplot(fig)
