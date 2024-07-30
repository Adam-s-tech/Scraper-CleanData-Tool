import streamlit as st
import numpy as np


def get_input_based_on_type(column_type, lang):
    if column_type == np.int64:
        return st.number_input("Nouvelle valeur" if lang == 'Fr' else "New value", format="%i")
    elif column_type == np.float64:
        return st.number_input("Nouvelle valeur" if lang == 'Fr' else "New value")
    elif column_type == np.bool_ or column_type == bool:
        return st.checkbox("Nouvelle valeur" if lang == 'Fr' else "New value")
    elif column_type == 'datetime64[ns]':
        return st.date_input("Nouvelle valeur" if lang == 'Fr' else "New value")
    else:  # Assume string
        return st.text_input("Nouvelle valeur" if lang == 'Fr' else "New value")