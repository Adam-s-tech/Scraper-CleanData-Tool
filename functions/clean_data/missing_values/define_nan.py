import streamlit as st 
import base64


def nan_to_define(data, column_to_modify, user_input, file_name, lang):
    # Analyze the type of the selected column
    column_type = data[column_to_modify].dtype
    st.text("Type de la colonne : " + str(column_type) if lang == 'Fr' else 
            "Type of the column : " + str(column_type))

    # Calculate the number of missing values in the selected column
    num_missing_values = data[column_to_modify].isna().sum()
    st.text("Nombre de valeurs manquantes : " + str(num_missing_values) if lang == 'Fr' else 
            "Number of missing values : " + str(num_missing_values))

    # Add a replace button to the sidebar
    if st.button("Remplacer" if lang == 'Fr' else "Replace"):
        # Replace missing values with the user input
        data[column_to_modify] = data[column_to_modify].fillna(user_input)
        st.write(data)

        # Convert DataFrame to CSV
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
        st.markdown(href, unsafe_allow_html=True)
