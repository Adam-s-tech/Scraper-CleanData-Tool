import streamlit as st 
import pandas as pd
import base64


def convert_col_types(chosen_type, data, column_to_modify, file_name, lang):
    # Convert the column to the chosen data type
    try:
        if chosen_type == 'date':
            data[column_to_modify] = pd.to_datetime(data[column_to_modify])
        else:
            data[column_to_modify] = data[column_to_modify].astype(chosen_type)
            
        # Convert DataFrame to CSV
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("La conversion a réussi." if lang == 'Fr' else "Conversion successful.")
    except Exception as e:
        st.error("La conversion a échoué : {}".format(e) if lang == 'Fr' else "Conversion failed : {}".format(e))