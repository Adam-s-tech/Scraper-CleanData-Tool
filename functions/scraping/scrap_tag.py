import streamlit as st
import pandas as pd
import base64
import requests
import subprocess
import json
import os
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def scrap_tag(url, selected_tags, lang):
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    scrap_js_web = False
    
    dfs = []
    for tag in selected_tags:
        elements = soup.find_all(tag)
        data = {tag: [element.text for element in elements]}
        df = pd.DataFrame(data)
        if not df.empty and not scrap_js_web:
            dfs.append(df)
        else:
            scrap_js_web = True

            # Get the absolute path of the project root & Define path to virtual environment's activate script
            project_root = os.path.dirname(os.path.abspath(__file__))
            activate_script_path = os.path.join(project_root, "..", "..", ".env", "Scripts", "activate")

            # Define the path to the Python script
            python_script_dir = os.path.join(project_root, "..", "..", "functions", "scraping", "scrap_js_website")
            python_script_name = "scrap_js.py"

            # Convert the arguments to JSON format
            args = json.dumps({"url": url, "tags": selected_tags}).replace('"', '\\"')

            # Define the command to activate the environment and run the script
            cmd = f'{activate_script_path} && cd {python_script_dir} && python {python_script_name} "{args}"'

            # Run the command
            subprocess.Popen(cmd, shell=True)

    # If scrap_js_web is True, read the data from the JSON file
    if scrap_js_web:
        if lang == 'Fr':
            st.warning(f"Tentative de scrap avec navigateur et rendu js pour les sites en React, ViteJS...")
        else: 
            st.warning(f"Attempt at scrapping with browser and js rendering for sites in React, ViteJS...")

        time.sleep(2)
    
        # Get the absolute path of the project root
        project_root = os.path.dirname(os.path.abspath(__file__))

        # Define the path to the JSON file
        json_file_path = os.path.join(project_root, "scrap_js_website", "scraped_data.json")
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            for tag, elements in data.items():
                df = pd.DataFrame({tag: elements})
                dfs.append(df)

    # Check if dfs is not empty before concatenating
    if dfs:
        final_df = pd.concat(dfs, axis=1)

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