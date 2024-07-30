import streamlit as st
import os
from functions.title_function import set_page_title


def main():
    # Add a language switcher to the sidebar
    lang = st.sidebar.selectbox('🔤 Language', ['Fr', 'En'])

    # Add a file uploader to the sidebar
    exe_file = st.sidebar.file_uploader("Mettez votre chrome.exe" if lang == 'Fr' else "Put your chrome.exe", type=['exe'])

    # If a file is uploaded, write the file path to a text file
    if exe_file is not None:
        base_path = os.path.dirname(os.path.abspath(exe_file.name))
        exe_name = os.path.basename(exe_file.name)
        chrome_path = os.path.join(base_path, 'chrome-win', exe_name)
        with open('./functions/scraping/scrap_js_website/chrome_path.txt', 'w') as f:
            f.write(chrome_path)
            st.sidebar.success("Maintenant vous n'avez plus besoin de remettre votre chrome.exe." if lang == 'Fr' else 
                               "Now you don't have to hand over your chrome.exe.")

    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

    # Add a title that changes based on the language
    if lang == 'Fr':
        st.title("Outil de Nettoyage de Données & Scraping")
        st.write("Interface permettant de scrapper facilement et rapidement des sites. \
                 L'outil possède également une section permettant le nettoyage des données.")
        st.markdown("""Vous pouvez :        
                - ⛏️ Scraper une ou plusieurs pages.    
                - 🧹 Nettoyage des données.     
                - 📊 Gérer les données.         
                """)
    else:
        st.title("Scrapper & Clean Data Tool")
        st.write("Interface to scrape sites easily and quickly. \
                 The tool also has a section for data cleaning.")
        st.markdown("""You can :        
                - ⛏️ Scrape one or more pages.      
                - 🧹 Data cleaning.         
                - 📊 Manage data.       
                """)

    # Use the function to set the page title
    set_page_title("menu · Streamlit", "🛠️Menu")

if __name__ == "__main__":
    main()