import streamlit as st
import pandas as pd
import base64


def one_hot_encoding(data, column_to_modify, file_name, lang):
    if data[column_to_modify].dtype in ['int64', 'float64', 'datetime64[ns]']:
        st.error("Erreur, vous ne pouvez pas encoder sur une colonne de Type Int, Float ou Datetime" if lang == 'Fr' else 
                 "Error, You Can't Encode on a Column of Type Int, Float, or Datetime")
    else:
        # Add a button for encoding
        if st.button('Encoder' if lang == 'Fr' else "Encode"):
            # Check if the column's data type is not date, int, or float
            if data[column_to_modify].dtype not in ['int64', 'float64', 'datetime64[ns]']:
                # Hot-encoding the column
                data = pd.get_dummies(data, columns=[column_to_modify])
                st.write(data)

                # Convert DataFrame to CSV
                csv = data.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
                st.markdown(href, unsafe_allow_html=True)