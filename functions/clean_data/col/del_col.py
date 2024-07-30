import streamlit as st
import base64


def del_col(data, columns_to_delete, file_name, lang):
    # Delete selected columns
    data = data.drop(columns=columns_to_delete)

    # View updated data in the Streamlit app
    st.write(data)

    # Convert DataFrame to CSV
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
    st.markdown(href, unsafe_allow_html=True)