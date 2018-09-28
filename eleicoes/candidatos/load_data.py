# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 13:05:38 2018

@author: aderson.medeiros
"""

import requests
import io
import os
import zipfile
import re
from bs4 import BeautifulSoup

def descompactarCandidatos(url):
    
    base_path = 'data/'
    
    info_paths = requests.get(url)
    soup = BeautifulSoup(info_paths.text, 'html.parser')
    info_individual_path = [(url + link.get('href')) for link in soup.find_all('a') if re.search('^[a-zA-Z].*', link.get('href'))]
    
    for info_path in info_individual_path:
        individual_path = requests.get(info_path)
        soup = BeautifulSoup(individual_path.text, 'html.parser')
        link_result = [info_path + link.get('href') for link in soup.find_all('a') if re.search('.*2018.*', link.get('href'))]
        
        if len(link_result) > 0:
            for link in link_result:
                zip_file = requests.get(link)
                with zipfile.ZipFile(io.BytesIO(zip_file.content)) as arquivo_candidatos:
                    if not os.path.isdir(base_path):
                        os.mkdir()
                    
                    specific_path = link.rsplit('/')[-1].split('.')[0] + '/'
                    arquivo_candidatos.extractall(base_path + specific_path)