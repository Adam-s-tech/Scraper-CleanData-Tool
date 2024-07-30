import streamlit as st
import base64
from sklearn.preprocessing import OrdinalEncoder


def ordinal_encoding(data, columns_to_modify, file_name, lang):
    cant_encode = False

    # Add a button for encoding
    if st.button('Encoder' if lang == 'Fr' else "Encode"):
        for column_to_modify in columns_to_modify:
            if data[column_to_modify].dtype in ['int64', 'float64', 'datetime64[ns]']:
                cant_encode = True
                st.error(f"Erreur, vous ne pouvez pas encoder sur la colonne **{column_to_modify}** de Type Int, Float ou Datetime" if lang == 'Fr' else 
                         f"Error, You Can't Encode on the Column **{column_to_modify}** of Type Int, Float, or Datetime")
            else:
                # Check if the column's data type is not date, int, or float
                if data[column_to_modify].dtype not in ['int64', 'float64', 'datetime64[ns]']:
                    # Ordinal encoding the column
                    oe = OrdinalEncoder()
                    data[column_to_modify] = oe.fit_transform(data[[column_to_modify]])

        if not cant_encode:
            st.write(data)

            # Convert DataFrame to CSV
            csv = data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
            st.markdown(href, unsafe_allow_html=True)
