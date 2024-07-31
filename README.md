# Data Analysis and Visualization with Streamlit

This project is a data analysis and visualization project that uses Streamlit to create interactive visualizations. The data used in this project is a CSV file containing information about documents and targets. The data is preprocessed and analyzed to identify relationships between different levels and categories.

## Prerequisites

- Python 3.9 or later
- Streamlit
- Pandas
- Plotly

## Installation

1. Clone the repository:

```bash
git clone https://github.com/chewnusi/data-analysis
```

2. To install the required packages, run the following command:

```bash
pip install streamlit pandas plotly
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## Usage

The Streamlit app provides interactive visualizations based on the data analysis. The app displays the following visualizations:

1. Hierarchical relationships between document and target levels
2. Distribution of document and target levels
3. Count of document and target types within each department
4. Relationship between document types and target types
5. Distribution of document types within L0 levels
6. Distribution of target types within target L0 levels

The app also provides a download link to download the processed (cleaned) data.

## Functions overview

1. `clean_data(df)`: Clean the data by removing duplicates and null values.
2. `explore_hierarchy(df)`: Explore the hierarchical relationships between different levels.
3. `plot_hierarchy(df)`: Plot the hierarchical relationships between document and target levels.
4. `plot_l0_tl0(df)`: Plot the distribution of document and target levels.
5. `plot_department_doctype(df)`: Plot the count of document and target types within each department.
6. `plot_doctype_targetype(df)`: Plot the relationship between document types and target types.
7. `plot_l0_doctype(df)`: Plot the distribution of document types within L0 levels.
8. `plot_tl0_targetype(df)`: Plot the distribution of target types within target L0 levels.
9. `prepare_data(file_path)`: Load the data from a CSV file.
10. `save_to_csv(df)`: Save the processed data to a CSV file.
11. `get_table_download_link(df)`: Generate a download link for the processed data.

## Conclusion

The visualizations show clear patterns and relationships between different levels and categories. The data analysis reveals that documents and targets have distinct categories at different levels, with some unique values in the detailed levels that are not shared between documents and targets. Departments have a similar pattern, with certain document and target types being more common.

## Results

The app is deployed on Streamlit Sharing and can be accessed [here](https://data-analysis-and-visualisation.streamlit.app/).