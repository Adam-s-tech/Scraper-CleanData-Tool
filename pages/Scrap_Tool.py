import streamlit as st
from functions.title_function import set_page_title
from functions.scraping.scrap_tag import scrap_tag
from functions.scraping.scrap_tag_all_site import scrap_all_site


# Add a language switcher to the sidebar
lang = st.sidebar.selectbox('🔤 Language', ['Fr', 'En'])

st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

# Input for website URL
url = st.sidebar.text_input("Mettre le Site Web" if lang == 'Fr' else "Input Website", "")

# Check if the input is a valid http or https URL
if url.startswith('http://') or url.startswith('https://'):
    st.sidebar.markdown("<hr style='margin:3px;'>", unsafe_allow_html=True)

    # Add a button to the sidebar to choose between "scrap page" and "scrap all site"
    scrap_choices = ["Scrap une Page", "Scrap tout un Site"] if lang == 'Fr' else ["Scrap a Page", "Scrap all Site"]
    scrap_choice = st.sidebar.radio("Choix de scrap" if lang == 'Fr' else "Choice of scrap", scrap_choices)

    if scrap_choice == scrap_choices[0]:
        st.title("📃Scrap une Page" if lang == 'Fr' else "📃Scrap a Page")
    else: 
        st.title("📘Scrap tout un Site" if lang == 'Fr' else "📘Scrap all Site")

    # Display a list in the main window
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'div', 'span', 'img', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th']
    selected_tags = st.multiselect("Choisissez les balises à scraper" if lang == 'Fr' else "Choose the tags to scrap", tags)
    if not selected_tags:
        st.warning("Choisissez les balises à scraper" if lang == 'Fr' else "Choose the tags to scrap")

    # If user want to scrap all the site
    if scrap_choice == scrap_choices[1]:
        # Add a number input to the sidebar to choose the maximum number of pages to scrap
        max_pages = st.sidebar.number_input('Nombre maximum de pages à scraper' if lang == 'Fr' else 
                                            'Maximum number of pages to scrap', min_value=1, value=5)

    if selected_tags:
        if st.button('Scrap'):
            if scrap_choice == scrap_choices[0]:
                scrap_tag(url, selected_tags, lang)
            else:
                scrap_all_site(url, selected_tags, max_pages, lang)
else:
    if lang =='Fr':
        st.sidebar.warning("Veuillez entrer une URL valide commençant par http:// ou https://")
    else:
        st.sidebar.warning("Please enter a valid URL starting with http:// or https://")

# Use the function to set the page title
set_page_title("Scrap_Tool · Streamlit", "⛏️ Outil Scraper" if lang =='Fr' else "⛏️ Scraper Tool")