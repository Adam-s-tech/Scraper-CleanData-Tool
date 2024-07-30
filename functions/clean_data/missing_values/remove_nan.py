import streamlit as st 
import base64


def remove_nan(data, column_to_modify, file_name, lang):
    # Calculate the number of missing values in the selected column
    num_missing_values = data[column_to_modify].isna().sum()
    st.text("Nombre de valeurs manquantes : " + str(num_missing_values) if lang == 'Fr' else 
            "Number of missing values : " + str(num_missing_values))

    # Add a remove button to the sidebar
    if st.button("Supprimer" if lang == 'Fr' else "Remove"):
        # Remove rows with missing values
        data.dropna(subset=[column_to_modify], inplace=True)
        st.write(data)

        # Convert DataFrame to CSV
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
        st.markdown(href, unsafe_allow_html=True)
