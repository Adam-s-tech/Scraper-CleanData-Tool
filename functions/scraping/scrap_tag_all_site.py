import streamlit as st
import requests
import time
import pandas as pd
import base64
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urlparse, urljoin


def is_valid(url, base_url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and base_url in url

def scrap_page(url, selected_tags, index):
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    dfs = []
    empty_tags = set()
    for tag in selected_tags:
        elements = soup.find_all(tag)
        data = {f"{tag}_{index}": [element.text for element in elements]}
        df = pd.DataFrame(data)
        if df.empty:
            empty_tags.add(tag)
        else:
            dfs.append(df)

    # Finding all internal links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            next_url = urljoin(url, href)
            if is_valid(next_url, urlparse(url).netloc):
                links.append(next_url)

    return dfs, links, empty_tags

def scrap_all_site(start_url, selected_tags, max_pages, lang):
    visited = set()
    to_visit = [start_url]
    all_dfs = []
    max_pages = int(max_pages)
    all_empty_tags = set()

    index = 0  # Initialize a global index

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url not in visited:
            visited.add(url)
            dfs, links, empty_tags = scrap_page(url, selected_tags, index)
            index += 1  # Increment the index
            all_dfs.extend(dfs)
            to_visit.extend(links)
            all_empty_tags.update(empty_tags)
            time.sleep(0.5)  # Respect online politeness by not overloading the server

    # Display warnings for empty tags
    for tag in all_empty_tags:
        if lang == 'Fr':
            st.warning(f"Il n'y a pas d'élément dans certaines pages pour la balise {tag}")
        else: 
            st.warning(f"There's no element in some pages for the {tag}")

    # Check if all_dfs is not empty before concatenating
    if all_dfs:
        final_df = pd.concat(all_dfs, axis=1)

        # Show scrap data
        st.write(final_df)

        csv = final_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        if lang == 'Fr':
            href = f'<a href="data:file/csv;base64,{b64}" download="scraped_data.csv">Télécharger le fichier CSV</a>'
        else: 
            href = f'<a href="data:file/csv;base64,{b64}" download="scraped_data.csv">Download CSV file</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        if lang == 'Fr':
            st.warning("Il n'y a rien à scraper")
        else:
            st.warning("There's nothing to scrap")