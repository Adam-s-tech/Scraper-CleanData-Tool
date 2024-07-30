import streamlit as st 
import base64


def select_interval(data, column_to_modify, start, end, file_name, lang):
    # If the user has not defined a start, we take 0 by default
    if start is None:
        start = 0

    # Create a copy of the data
    data_copy = data.copy()

    # Process the specified interval for each value in the column
    for i in range(len(data_copy)):
        column_value = str(data_copy.loc[i, column_to_modify])
        if end is None or end > len(column_value):
            end = len(column_value)
        data_copy.loc[i, column_to_modify] = column_value[start:end]

    # Add a button for the user to select the interval and download the CSV
    if st.button("Sélectionnez Intervalle" if lang == 'Fr' else "Select Interval"):
        st.write(data_copy)

        # Convert DataFrame to CSV
        csv = data_copy.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
        st.markdown(href, unsafe_allow_html=True)