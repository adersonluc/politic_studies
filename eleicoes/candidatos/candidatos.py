import pandas as pd
import load_data
import os

ABS_PATH = 'http://agencia.tse.jus.br/estatistica/sead/odsele/'

CANDIDATOS_URL = ABS_PATH + 'consulta_cand/consulta_cand_2018.zip'

#load_data.descompactarCandidatos(ABS_PATH)

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
