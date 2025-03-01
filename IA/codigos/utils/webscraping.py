import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()

driver.get("http://sigtap.datasus.gov.br/tabela-unificada/app/sec/procedimento/publicados/consultar")

c_field = driver.find_element("id", "acessoAutomatico")
c_field.click()

driver.implicitly_wait(3)

lupa_field = driver.find_element("id", "formConsultarProcedimento:localizar")
lupa_field.click()

last_page = driver.find_element("id", "formConsultarProcedimento:pageslast")
last_page.click()

number_last_page = int(driver.find_element('id', "formConsultarProcedimento:pagesidx554_text").text)

driver.implicitly_wait(3)

back_to_first_page = driver.find_element("id", "formConsultarProcedimento:pagesfirst").click()

file = open("procedimentos2.txt", 'w')

for j in range(1, number_last_page+1):
    for i in range(1, 11):
        table_field = driver.find_element("xpath", f"/html/body/div/div[3]/form/table[2]/tbody/tr[{i}]")
        first_part = table_field.text.split(" - ", 1)[0]
        second_part = table_field.text.split(" - ", 1)[1]
        file.write(f'"{first_part}", "{second_part}"' + '\n')
        

    next_page_button = driver.find_element("id", "formConsultarProcedimento:pagesnext")
    next_page_button.click()

file.close()




