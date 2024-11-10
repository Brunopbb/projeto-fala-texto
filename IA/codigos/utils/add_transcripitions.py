from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd

def get_transcriptions():

    df = pd.read_csv('/home/brunoee/Documentos/projeto/procedimentosCorrigidos.txt', sep=',', quotechar='"', on_bad_lines='skip', names=['transcrição'])
    df = df.map(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    
    array = np.array(df['transcrição'])
    return array

procedimentos = get_transcriptions()


driver = webdriver.Firefox()

driver.get("https://fala-texto.zapto.org/add_transcription")
driver.implicitly_wait(5)


for procedimento in procedimentos:

    transcription_field = driver.find_element("id", "transcription")
    transcription_field.send_keys(procedimento)

    driver.find_element("id", "addTranscriptionBtn").click()
    driver.implicitly_wait(3)


    if driver.find_element("id", "responseMessage").text == "A transcrição já existe no banco de dados.":
        transcription_field.clear()
        driver.implicitly_wait(3)
        continue

    driver.implicitly_wait(3)
    





