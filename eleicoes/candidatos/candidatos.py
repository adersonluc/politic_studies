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

def descompactarCandidatos(url, path):
    if not os.path.isdir(path):
        os.mkdir(path)
        
    info_paths = requests.get(url)
    soup = BeautifulSoup(info_paths.text, 'html.parser')
    info_individual_path = [(url + link.get('href')) for link in soup.find_all('a') if re.search('^[a-zA-Z].*', link.get('href'))]
    
    link_info = []
    for info_path in info_individual_path:
        individual_path = requests.get(info_path)
        soup = BeautifulSoup(individual_path.text, 'html.parser')
        link_result = [info_path + link.get('href') for link in soup.find_all('a') if re.search('.*2018.*', link.get('href'))]
        
        if len(link_result) > 0:
            for link in link_result:
                zip_file = requests.get(link)
                with zipfile.ZipFile(io.BytesIO(zip_file.content)) as arquivo_candidatos:
                    if not os.path.isdir('data/'):
                        os.mkdir()
                    
                    arquivo_candidatos.extractall()

import pandas as pd

ABS_PATH = 'http://agencia.tse.jus.br/estatistica/sead/odsele/'

CANDIDATOS_URL = ABS_PATH + 'consulta_cand/consulta_cand_2018.zip'
PATH_CANDIDATOS = 'data'

descompactarCandidatos(ABS_PATH, PATH_CANDIDATOS)

resultado = os.listdir(os.getcwd() + '/data')
data_final = pd.DataFrame()
for rest in resultado:
    if re.search('.csv', rest):
       with open('data/' + rest) as uf:
           data = pd.read_csv(uf, sep=';', encoding='ISO-8859-1')
           if len(data_final) == 0:
               data_final = data
           else:
               data_final = data_final.append(data)

data_final.info()

zita = data_final[data_final['NR_CPF_CANDIDATO'] == 51215276249]
