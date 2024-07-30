import streamlit as st 
import numpy as np
import base64


def nan_to_mode(data, column_to_modify, file_name, lang):
    # Analyze the type of the selected column
    column_type = data[column_to_modify].dtype

    # If the column type is not int or float, calculate the mode
    if column_type not in [np.int64, np.float64]:
        # Calculate the number of missing values in the selected column
        num_missing_values = data[column_to_modify].isna().sum()
        st.text("Nombre de valeurs manquantes : " + str(num_missing_values) if lang == 'Fr' else 
                "Number of missing values : " + str(num_missing_values))

        # Calculate the mode of the selected column
        mode_value = data[column_to_modify].mode()[0]
        st.text("Mode de la colonne : " + str(mode_value) if lang == 'Fr' else 
                "Mode of the column : " + str(mode_value))

        # Add a replace button to the sidebar
        if st.button("Remplacer" if lang == 'Fr' else "Replace"):
            # Replace missing values with the mode
            data[column_to_modify] = data[column_to_modify].fillna(mode_value)
            st.write(data)

            # Convert DataFrame to CSV
            csv = data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("Erreur : La colonne sélectionnée est de type int ou float." if lang == 'Fr' else 
                 "Error: The selected column is of type int or float.")