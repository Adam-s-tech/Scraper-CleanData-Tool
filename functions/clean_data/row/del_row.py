import streamlit as st
import base64


def del_row(data, start, end, file_name, lang):
    # Delete selected rows
    data = data.drop(data.index[start:end])

    # View updated data in the Streamlit app
    st.write(data)

    # Convert DataFrame to CSV
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{"Télécharger le fichier CSV" if lang == "Fr" else "Download CSV file"}</a>'
    st.markdown(href, unsafe_allow_html=True)