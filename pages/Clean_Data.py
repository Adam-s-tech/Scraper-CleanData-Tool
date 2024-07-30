import streamlit as st
import pandas as pd
import os
from functions.title_function import set_page_title
from functions.clean_data.col.del_col import del_col
from functions.clean_data.col.rename_col import rename_col
from functions.clean_data.col.get_col_type import get_input_based_on_type
from functions.clean_data.row.del_row import del_row
from functions.clean_data.row.modify_row import modify_row
from functions.clean_data.missing_values.remove_nan import remove_nan
from functions.clean_data.missing_values.number.replace_with_mean import nan_to_mean
from functions.clean_data.missing_values.number.replace_with_std import nan_to_std
from functions.clean_data.missing_values.number.replace_with_median import nan_to_median
from functions.clean_data.missing_values.replace_with_mode import nan_to_mode
from functions.clean_data.missing_values.define_nan import nan_to_define
from functions.clean_data.transformations.convert_types import convert_col_types
from functions.clean_data.transformations.select_interval import select_interval
from functions.clean_data.transformations.one_hot import one_hot_encoding
from functions.clean_data.transformations.label_encoder import label_encoding
from functions.clean_data.transformations.ordinal_encoder import ordinal_encoding


# Add a language switcher to the sidebar
lang = st.sidebar.selectbox('🔤 Language', ['Fr', 'En'])

st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

# Add a file upload button to the sidebar
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier CSV" if lang == 'Fr' else
                                         "Choose a CSV file", type="csv")

st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

# Check if a file has been downloaded
if uploaded_file is not None:
    # Get the file name and add "_clean" at the end
    file_name = os.path.splitext(uploaded_file.name)[0] + "_clean.csv"

    # Read CSV file with pandas
    data = pd.read_csv(uploaded_file)

    # View data in the Streamlit app
    st.write(data)

    st.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

    st.sidebar.title('Colonnes' if lang == 'Fr' else 'Columns')

    # Add a checkbox to the sidebar
    del_col_check = st.sidebar.checkbox("❌Supprimer Colonnes" if lang == 'Fr' else "❌Delete Columns")

    # Add a checkbox to the sidebar for renaming columns
    rename_col_check = st.sidebar.checkbox("🔄Renommer une Colonne" if lang == 'Fr' else "🔄Rename Column")

    st.sidebar.title('Lignes' if lang == 'Fr' else 'Rows')

    # Add a checkbox to the sidebar for deleting rows
    del_row_check = st.sidebar.checkbox("❌Supprimer Lignes" if lang == 'Fr' else "❌Delete Rows")

    # Add a checkbox to the sidebar for modify rows
    mod_row_check = st.sidebar.checkbox("⚙️Modifier Lignes" if lang == 'Fr' else "⚙️Modify Rows")

    st.sidebar.title('Valeurs Manquantes' if lang == 'Fr' else 'Missing Values')

    # Add a checkbox to the sidebar for missing values
    miss_val_remove_check = st.sidebar.checkbox("❌Supprime" if lang == 'Fr' else "❌Delete")
    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)
    miss_val_mean_check = st.sidebar.checkbox("🧮Moyenne" if lang == 'Fr' else "🧮Mean")
    miss_val_std_check = st.sidebar.checkbox("➗Écart-Type" if lang == 'Fr' else "➗Standard Deviation")
    miss_val_median_check = st.sidebar.checkbox("🟰Médiane" if lang == 'Fr' else "🟰Median")
    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)
    miss_val_mode_check = st.sidebar.checkbox("Mode" if lang == 'Fr' else "Mode")
    miss_val_def_check = st.sidebar.checkbox("Définir" if lang == 'Fr' else "Define")

    st.sidebar.title('Transformations')

    transfo_types_check = st.sidebar.checkbox("Modifier Types" if lang == 'Fr' else "Modify Types")
    transfo_interval_check = st.sidebar.checkbox("Modifier Intervalle" if lang == 'Fr' else "Modify Interval")
    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)
    transfo_onehot_check = st.sidebar.checkbox("One Hot")
    transfo_label_check = st.sidebar.checkbox("Label Encoding")
    transfo_ordinal_check = st.sidebar.checkbox("Ordinal Encoding")
    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

    if del_col_check:
        # Add a multi-column selector
        columns_to_delete = st.multiselect("Sélectionnez les colonnes à supprimer" if lang == 'Fr' else
                                           "Select columns to delete", data.columns.tolist())

        # Add a column delete button
        if st.button("Supprimer les colonnes sélectionnées" if lang == 'Fr' else "Delete selected columns"):
            del_col(data, columns_to_delete, file_name, lang)

    if rename_col_check:
        # Add a single column selector
        column_to_rename = st.selectbox("Sélectionnez la colonne à renommer" if lang == 'Fr' else
                                        "Select column to rename", data.columns.tolist())
        # Add a text input
        new_name = st.text_input("Entrez le nouveau nom" if lang == 'Fr' else "Enter new name")

        # Add a rename button
        if st.button("Renommer la colonne sélectionnée" if lang == 'Fr' else "Rename selected column"):
            rename_col(data, column_to_rename, new_name, file_name, lang)

    if del_row_check:
        # Add a number input for the start & end of the range
        start = st.number_input("Début de l'intervalle" if lang == 'Fr' else "Start of range", min_value=0, max_value=len(data)-1)
        end = st.number_input("Fin de l'intervalle" if lang == 'Fr' else "End of range", min_value=start, max_value=len(data)-1)

        # Add a row delete button
        if st.button("Supprimer les lignes sélectionnées" if lang == 'Fr' else "Delete selected rows"):
            del_row(data, start, end, file_name, lang)

    if mod_row_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne à modifier" if lang == 'Fr' else "Choose column to modify", data.columns)
        
        # Add a number input for the start & end of the range
        start = st.number_input("Début de l'intervalle" if lang == 'Fr' else "Start of range", min_value=0, max_value=len(data)-1)
        end = st.number_input("Fin de l'intervalle" if lang == 'Fr' else "End of range", min_value=start, max_value=len(data)-1)

        # Analyze the type of the selected column
        column_type = data[column_to_modify].dtype

        # Display an input field adapted to the type of the column
        new_value = get_input_based_on_type(column_type, lang)

        # Add a modify button
        if st.button("Modifier les lignes sélectionnées" if lang == 'Fr' else "Modify selected rows"):
            modify_row(data, column_to_modify, start, end, new_value, file_name, lang)

    if miss_val_remove_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        remove_nan(data, column_to_modify, file_name, lang)

    if miss_val_mean_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        nan_to_mean(data, column_to_modify, file_name, lang)

    if miss_val_std_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        nan_to_std(data, column_to_modify, file_name, lang)

    if miss_val_median_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        nan_to_median(data, column_to_modify, file_name, lang)

    if miss_val_mode_check:
        # Add a selectbox for the column to modify
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        nan_to_mode(data, column_to_modify, file_name, lang)

    if miss_val_def_check:
        # Add a selectbox for the column to modify & define the data types
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        data_types = ['bool', 'int', 'float', 'string', 'object', 'date']
        data_type = st.selectbox("Choisir le type de données" if lang == 'Fr' else "Choose data type", data_types)

        # Add a user input field based on the selected data type
        if data_type == 'bool':
            user_input = st.checkbox("Entrez une valeur" if lang == 'Fr' else "Enter a value")
        elif data_type in ['int', 'float']:
            user_input = st.number_input("Entrez une valeur" if lang == 'Fr' else "Enter a value")
        elif data_type == 'date':
            user_input = st.date_input("Entrez une valeur" if lang == 'Fr' else "Enter a value")
        else:
            user_input = st.text_input("Entrez une valeur" if lang == 'Fr' else "Enter a value")
        nan_to_define(data, column_to_modify, user_input, file_name, lang)

    if transfo_types_check:
        # Add a selectbox for the column to modify & define the data types
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)

        # Display the current data type of the selected column
        st.write("Type actuel de la colonne :" if lang == 'Fr' else "Actual type of the column", data[column_to_modify].dtype)
        
        # Define the data types that the user can choose from
        data_types = ['bool', 'int', 'float', 'string', 'date', 'object']
        
        # Add a selectbox for the data type
        chosen_type = st.selectbox("Choisir le type de données" if lang == 'Fr' else "Choose data type", data_types)
        
        # Add a button for the user to click to convert the column
        if st.button("Convertir" if lang == 'Fr' else "Convert"):
            convert_col_types(chosen_type, data, column_to_modify, file_name, lang)

    if transfo_interval_check:
        # Add a selectbox for the column to be modified & define the data types
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        
        # Add a text input for the start & end
        start = st.text_input("Début de l'intervalle" if lang == 'Fr' else "Start of range")
        end = st.text_input("Fin de l'intervalle" if lang == 'Fr' else "End of range")
        
        # Convert inputs to integers if they are not empty
        start = int(start) if start else None
        end = int(end) if end else None
        select_interval(data, column_to_modify, start, end, file_name, lang)

    if transfo_onehot_check:
        # Add a selection box for the column to be edited and define the data types
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        one_hot_encoding(data, column_to_modify, file_name, lang)

    if transfo_label_check:
        # Add a selectbox for the column to be modified & define the data types
        column_to_modify = st.selectbox("Choisir la colonne" if lang == 'Fr' else "Choose column", data.columns)
        label_encoding(data, column_to_modify, file_name, lang)

    if transfo_ordinal_check:
        # Add a multiselect for the columns to be modified & define the data types
        columns_to_modify = st.multiselect("Choisir les colonnes" if lang == 'Fr' else "Choose columns", data.columns)
        ordinal_encoding(data, columns_to_modify, file_name, lang)

# Use the function to set the page title
set_page_title("Clean_Data · Streamlit", "🧹 Nettoyage des Données" if lang =='Fr' else "🧹 Clean Data")