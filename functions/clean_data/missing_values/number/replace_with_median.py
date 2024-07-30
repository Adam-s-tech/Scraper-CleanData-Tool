import streamlit as st 
import numpy as np
import base64


def nan_to_median(data, column_to_modify, file_name, lang):
    # Analyze the type of the selected column
    column_type = data[column_to_modify].dtype

    # Check if the column type is int or float
    if column_type not in [np.int64, np.float64]:
        st.error("Erreur : La colonne sélectionnée n'est pas de type int ou float." if lang == 'Fr' else 
                 "Error: The selected column is not of type int or float.")
    else:
        # Calculate the number of missing values in the selected column
        num_missing_values = data[column_to_modify].isna().sum()
        st.text("Nombre de valeurs manquantes : " + str(num_missing_values) if lang == 'Fr' else 
                "Number of missing values : " + str(num_missing_values))

        # Calculate the median of the selected column
        median_value = data[column_to_modify].median()
        st.text("Médiane de la colonne : " + str(median_value) if lang == 'Fr' else 
                "Median of the column : " + str(median_value))

        # Add a replace button to the sidebar
        if st.button("Remplacer" if lang == 'Fr' else "Replace"):
            # Replace missing values with the median
            data[column_to_modify] = data[column_to_modify].fillna(median_value)
            st.write(data)

            # Convert DataFrame to CSV
            csv = data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
            st.markdown(href, unsafe_allow_html=True)
