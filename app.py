import streamlit as st
import pandas as pd
import plotly.express as px


def prepare_data(file_path):
    data = pd.read_csv(file_path, delimiter=';')
    df = pd.DataFrame(data)
    return df


def clean_data(df):
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    df = df.dropna()
    return df


def edit_columns(df):
    df[['Document Prefix', 'Document Number']] = df['Document name'].str.split('-', expand=True)
    df[['Target Prefix', 'Target Number']] = df['Target name'].str.split('-', expand=True)
    df['Doc Prefix vs Type Match'] = df['Document Prefix'] == df['Document type']
    df['Target Prefix vs Type Match'] = df['Target Prefix'] == df['Target type']
    df['Subcategory vs Doc Prefix Match'] = df['Subcategory'] == df['Document Prefix']

    df = df.drop(columns=['Document name', 'Target name', 'Document Prefix', 'Document Number', 'Target Prefix', 'Target Number', 'Subcategory', 'Doc Prefix vs Type Match', 'Target Prefix vs Type Match', 'Subcategory vs Doc Prefix Match'])
    return df


def explore_hierarchy(df):
    for level in ['L0', 'L1', 'L2']:
        doc_column = level
        target_column = 'Target ' + level

        doc_unique_values = df[doc_column].unique()
        target_unique_values = df[target_column].unique()

        # Additionally, if you want to compare and print the differences:
        common_values = set(doc_unique_values).intersection(target_unique_values)
        only_in_doc = set(doc_unique_values) - common_values
        only_in_target = set(target_unique_values) - common_values

        print(f"\nValues only in '{doc_column}' and not in '{target_column}':")
        print(only_in_doc)
        print(f"\nValues only in '{target_column}' and not in '{doc_column}':")
        print(only_in_target)


def save_to_csv(df):
    df.to_csv('DocumentsProcesses_adjusted.csv', sep=';', index=False)


def plot_hierarchy(df):
    # Mapping for short labels
    short_labels = {
        'Research and Development (R&D)': 'R&D',
        'Health, Safety, and Environment (HSE)': 'HSE',
        'Quality Control (QC)': 'QC',
        'Manufacturing': 'MFG'
    }

    # Replace L0 and Target L0 labels with short labels
    df['L0'] = df['L0'].replace(short_labels)
    df['Target L0'] = df['Target L0'].replace(short_labels)

    # Create a new DataFrame with a count of records for each unique value of 'L0'
    l0_counts = df['L0'].value_counts().reset_index()
    l0_counts.columns = ['L0', 'count']
    sorted_l0_counts = l0_counts.sort_values(by='count', ascending=False)

    # Create a dictionary to map 'L0' values to their sorted order
    sorted_l0_order = {val: idx for idx, val in enumerate(sorted_l0_counts['L0'])}
    df['L0_order'] = df['L0'].map(sorted_l0_order)

    # Create a new DataFrame with a count of records for each unique value of 'L1' within 'L0'
    l1_counts = df.groupby(['L0', 'L1']).size().reset_index(name='count')
    l1_counts = l1_counts.sort_values(by=['L0', 'count'], ascending=[True, False])

    # Create a dictionary to map 'L1' values to their sorted order within each 'L0'
    l1_order_dict = {}
    for l0 in l1_counts['L0'].unique():
        sorted_l1_values = l1_counts[l1_counts['L0'] == l0].sort_values(by='count', ascending=False)['L1']
        l1_order_dict.update({(l0, l1): idx for idx, l1 in enumerate(sorted_l1_values)})

    df['L1_order'] = df.apply(lambda row: l1_order_dict[(row['L0'], row['L1'])], axis=1)

    # Create a new DataFrame with a count of records for each unique value of 'L2' within 'L1'
    l2_counts = df.groupby(['L0', 'L1', 'L2']).size().reset_index(name='count')
    l2_counts = l2_counts.sort_values(by=['L0', 'L1', 'count'], ascending=[True, True, False])

    # Create a dictionary to map 'L2' values to their sorted order within each 'L1'
    l2_order_dict = {}
    for l0 in l2_counts['L0'].unique():
        for l1 in l2_counts[l2_counts['L0'] == l0]['L1'].unique():
            sorted_l2_values = l2_counts[(l2_counts['L0'] == l0) & (l2_counts['L1'] == l1)].sort_values(by='count', ascending=False)['L2']
            l2_order_dict.update({(l0, l1, l2): idx for idx, l2 in enumerate(sorted_l2_values)})

    df['L2_order'] = df.apply(lambda row: l2_order_dict[(row['L0'], row['L1'], row['L2'])], axis=1)

    # Sorting for Target L2, Target L1, Target L0
    # Creating similar mappings and sorted orders for Target L2, Target L1, and Target L0
    target_l0_counts = df['Target L0'].value_counts().reset_index()
    target_l0_counts.columns = ['Target L0', 'count']
    sorted_target_l0_counts = target_l0_counts.sort_values(by='count', ascending=False)
    sorted_target_l0_order = {val: idx for idx, val in enumerate(sorted_target_l0_counts['Target L0'])}
    df['Target_L0_order'] = df['Target L0'].map(sorted_target_l0_order)

    target_l1_counts = df.groupby(['Target L0', 'Target L1']).size().reset_index(name='count')
    target_l1_counts = target_l1_counts.sort_values(by=['Target L0', 'count'], ascending=[True, False])
    target_l1_order_dict = {}
    for target_l0 in target_l1_counts['Target L0'].unique():
        sorted_target_l1_values = target_l1_counts[target_l1_counts['Target L0'] == target_l0].sort_values(by='count', ascending=False)['Target L1']
        target_l1_order_dict.update({(target_l0, target_l1): idx for idx, target_l1 in enumerate(sorted_target_l1_values)})
    df['Target_L1_order'] = df.apply(lambda row: target_l1_order_dict[(row['Target L0'], row['Target L1'])], axis=1)

    target_l2_counts = df.groupby(['Target L0', 'Target L1', 'Target L2']).size().reset_index(name='count')
    target_l2_counts = target_l2_counts.sort_values(by=['Target L0', 'Target L1', 'count'], ascending=[True, True, False])
    target_l2_order_dict = {}
    for target_l0 in target_l2_counts['Target L0'].unique():
        for target_l1 in target_l2_counts[target_l2_counts['Target L0'] == target_l0]['Target L1'].unique():
            sorted_target_l2_values = target_l2_counts[(target_l2_counts['Target L0'] == target_l0) & (target_l2_counts['Target L1'] == target_l1)].sort_values(by='count', ascending=False)['Target L2']
            target_l2_order_dict.update({(target_l0, target_l1, target_l2): idx for idx, target_l2 in enumerate(sorted_target_l2_values)})
    df['Target_L2_order'] = df.apply(lambda row: target_l2_order_dict[(row['Target L0'], row['Target L1'], row['Target L2'])], axis=1)

    # Sort the DataFrame based on the sorted orders
    sorted_df = df.sort_values(['L0_order', 'L1_order', 'L2_order', 'Target_L2_order', 'Target_L1_order', 'Target_L0_order'])

    # Map L0 categories to a numeric value for coloring
    category_map = {cat: i for i, cat in enumerate(sorted_df['L0'].unique())}
    sorted_df['L0_color'] = sorted_df['L0'].map(category_map)

    # Define a color sequence
    colors = px.colors.qualitative.Plotly

    # Plotting
    fig = px.parallel_categories(sorted_df, dimensions=['L0', 'L1', 'L2', 'Target L2', 'Target L1', 'Target L0'], color='L0_color',
                                color_continuous_scale=colors,
                                labels={'L0_color': 'L0'})  # Adjust this if you want a different label

    fig.update_layout(coloraxis_showscale=False)

    st.plotly_chart(fig, use_container_width=True)  # Display the figure in Streamlit


def plot_l0_tl0(df):
    color_palette = px.colors.qualitative.Set3

    fig1 = px.sunburst(df, path=['L0', 'L1', 'L2'], 
                       hover_data=['L0', 'L1', 'L2'],
                       color_discrete_sequence=color_palette)  # Use custom color palette for fig1

    fig2 = px.sunburst(df, path=['Target L0', 'Target L1', 'Target L2'],
                       hover_data=['Target L0', 'Target L1', 'Target L2'],
                       color_discrete_sequence=color_palette)  # Use custom color palette for fig2

    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        st.plotly_chart(fig1, use_container_width=True)  # Display the first figure in the first column

    with col2:
        st.plotly_chart(fig2, use_container_width=True)


def plot_department_doctype(df):
    # Dropdown menu to select the category type
    category_type = st.selectbox('Select Category Type', ['Document type', 'Target type'])
    counts = df.groupby(['Department', category_type]).size().reset_index(name='counts')

    # Create the plot
    fig = px.bar(counts, x='Department', y='counts', color=category_type, text='counts',
                title=f'{category_type} categories by Department',
                labels={'counts': f'Count of {category_type}'},
                barmode='group')

    # Rotate x-axis tick labels
    fig.update_layout(xaxis_tickangle=0)

    st.plotly_chart(fig, use_container_width=True)


def plot_doctype_targetype(df):
    category_map = {cat: i for i, cat in enumerate(df['Document type'].unique())}
    df['Doc_color'] = df['Document type'].map(category_map)

    # Define a color sequence
    colors = px.colors.qualitative.Pastel

    fig = px.parallel_categories(df, dimensions=['Document type', 'Target type'],
                                 color='Doc_color',
                                 color_continuous_scale=colors,)
    fig.update_layout(coloraxis_showscale=False)
    # Show the figure
    st.plotly_chart(fig, use_container_width=True)


def plot_l0_doctype(df):
    # Prepare the data for the treemap
    df_grouped = df.groupby(['L0', 'Document type']).size().reset_index(name='count')

    # Plotting the treemap
    fig = px.treemap(
        df_grouped,
        path=['L0', 'Document type'],
        values='count',
        color='L0',
        custom_data=['L0', 'Document type', 'count']
    )

    # Update hover information to show detailed path and count
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Document Type: %{customdata[1]}<br>Count: %{customdata[2]}'
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)


def plot_tl0_targetype(df):
    # Prepare the data for the treemap
    df_grouped = df.groupby(['Target L0', 'Target type']).size().reset_index(name='count')

    # Plotting the treemap
    fig = px.treemap(
        df_grouped,
        path=['Target L0', 'Target type'],
        values='count',
        color='Target L0',
        custom_data=['Target L0', 'Target type', 'count']
    )

    # Update hover information to show detailed path and count
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Target Type: %{customdata[1]}<br>Count: %{customdata[2]}'
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Show the figure
    st.plotly_chart(fig, use_container_width=True)


def get_table_download_link(df):
    import base64
    csv = df.to_csv(index=False, sep=';')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="DocumentsProcesses_adjusted.csv">Click to download the processed data.</a>'
    return href


def main():
    file_path = './DocumentsProcesses_adjusted.csv'
    data = prepare_data(file_path)

    st.title('Test Assessment - Data Analysis')
    st.write("Me on LinkedIn: [**Katana Iryna**](https://www.linkedin.com/in/iryna-katana/)")
    st.write("Download CV: [**Iryna Katana CV**](https://drive.google.com/file/d/1SeO7HpozvkvORLrDmjNg4P_qBjBZHTgb/view?usp=drive_link)")
    st.write("This project GitHub: [**github.com/chewnusi/data-analysis**](https://github.com/chewnusi/data-analysis)")

    st.write("## Preprocessing Steps")
    st.write("""
    1. The data were loaded from csv file using `;` as the delimiter.
    2. The columns were stripped of whitespace.
    3. Duplicate records were removed (from 4179 to 4167).
    4. Rows with null values were dropped (the record 456 had NaN `Document name`).
    5. The `Document name` and `Target name` columns were split into prefixes and numbers.
    6. Boolean columns were created to check if the prefixes match the `Document type` and `Target type`.
    7. As all the prefixes matched the types, next columns were dropped: `Document name`, `Target name`, `Document Prefix`, `Document Number`, `Target Prefix`, `Target Number`, `Subcategory`, `Doc Prefix vs Type Match`, `Target Prefix vs Type Match`, `Subcategory vs Doc Prefix Match`.
    """)

    # Provide a download link for the processed data
    st.write("## Download Processed Data")
    st.markdown(get_table_download_link(data), unsafe_allow_html=True)

    st.write("## Data Analysis Results")
    st.write("### Hierarchical Relationships")
    plot_hierarchy(data)
    st.write("This graph shows the hierarchical relationships between the document and target levels. The colors represent the L0 categories of the documents. The thickness of the lines indicates the number of records. The graph is interactive, allowing to explore the relationships between different levels. ")
    st.write("After exploring the hierarchy it was found that each `L0` level has a unique set of `L1` and `L2` values. The same is true for the target levels. Each `Target L0` level has a unique set of `Target L1` and `Target L2` values.")
    st.write("However, there is no direct rule, that `L0` category should have the same `Target L0` category.")

    st.write("### Document and Target Levels")
    plot_l0_tl0(data)
    st.write("These sunburst charts illustrate more detailed distribution of documents and their corresponding target levels. In the center, you can see the L0 and Target L0 levels. Next, the L1 and Target L1 levels are shown. Finally, the outermost rings represent the L2 and Target L2 levels. The charts are interactive, allowing to choose specific categories.")
    st.write("The charts show that the Document and Target levels has the same categories for `L0` and `Target L0`, `L1` and `Target L1`. However, the `L2` level has 2 unique values that are not presented in `Target L2`. And `Target L2` has 8 values that are not presented in `L2`")

    st.write("### Department and Document/Target Types")
    plot_department_doctype(data)
    st.write("This bar chart highlights the count of different document or target types within each department. The pattern for document and target types is almost the same: Both departments show similar distribution pattern, with PRO being the most common document type, followed by INS and RD. RUL and STND are less common.")

    st.write("### Document Type and Target Type")
    plot_doctype_targetype(data)
    st.write("This diagram shows the relationship between document types and target types. It indicates that most document categories transition into PRO, followed by RD and INS.")

    st.write("### Document Types within L0 Levels")
    plot_l0_doctype(data)
    st.write("The treemap visualizes the distribution of document types within the L0 levels. All `L0` levels prioritize PRO document type. Other popular document types include INS and RD. What is important is that HSE has no STND and RUL document types, while MFG also has no STND")

    st.write("### Target Types within Target L0 Levels")
    plot_tl0_targetype(data)
    st.write("The treemap visualizes the distribution of target types within the target L0 levels. PRO is the most common target type for all `Target L0` levels. Other types are always presented in every level, but have different distribution.")

    st.write("## Conclusion")
    st.write("The relationships between document and target levels show clear patterns, with each having its own unique categories at different levels. Documents and targets share similar types, with PRO being the most common, followed by INS and RD. However, there are some unique values in the detailed levels that are not shared between documents and targets. Departments have a similar pattern, with certain document and target types being more common. Overall, the data shows clear but distinct categories for documents and targets.")


if __name__ == '__main__':
    main()
