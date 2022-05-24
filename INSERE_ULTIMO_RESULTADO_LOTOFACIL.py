#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pyodbc
import pandas as pd
server = 'DESKTOP-BAGV6SU\SQLEXPRESS01' 
database = 'LOTOFACIL' 
username = '' 
password = '' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
sorteio=pd.read_sql('''DECLARE @MAXIMO INT
SELECT @MAXIMO = MAX(ID_CONCURSO) FROM SORTEIOS
SELECT NUMERO_CONCURSO FROM SORTEIOS WHERE ID_CONCURSO = @MAXIMO''', cnxn)
cnxn.commit()
cursor.close()
conversao = sorteio.to_dict()
conversao = list(conversao.values())
numero_sorteio = conversao[0][0]
# importação
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#argumento de ocultação
chrome_options = Options()
chrome_options.add_argument('--headless')
# driver de funcionamento do navegador
driver = webdriver.Chrome(chrome_options=chrome_options)
# nome do site
driver.get("http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/")
# print(driver.title)
sorteado = []
i = 1                                
concurso = driver.find_element_by_xpath('//*[@id="resultados"]/div[1]/div/h2/span').text
concurso_novo = concurso[9:13]
concurso_novo = int(concurso_novo)

if numero_sorteio <concurso_novo:
    concurso = (concurso[:8] + "_" + concurso[9:13] + "_" + concurso[15:17] + '_' + concurso[18:20] + '_' + concurso[21:25])
    xpath = r'/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[3]/section/div[2]/div[2]/div/div/div[2]/div/div/div[1]/ul/li[{numero}]'
    for i in range(15):
        num_resultado = driver.find_element_by_xpath(xpath.format(numero = i + 1))
        numero = num_resultado.text
        numero = int(numero)
        sorteado.append(numero)
    i = 0

    cursor = cnxn.cursor()
    cursor.execute(f'''INSERT INTO RESULTADOS_FACIL$ (F1,F2,F3,F4,F5,
    F6,F7,F8,F9,F10,F11,F12,F13,F14,F15) values ({sorteado[0]},{sorteado[1]},{sorteado[2]},
    {sorteado[3]},{sorteado[4]},{sorteado[5]},{sorteado[6]},{sorteado[7]},{sorteado[8]},
    {sorteado[9]},{sorteado[10]},{sorteado[11]},{sorteado[12]},{sorteado[13]},{sorteado[14]})''')
    cnxn.commit()
    cursor.close()
    cursor = cnxn.cursor()
    cursor.execute(f'INSERT INTO SORTEIOS VALUES ({concurso_novo})')
    cnxn.commit()
    cursor.close()
    cursor = cnxn.cursor()
    cursor.execute('EXECUTE ATUALIZACAO_SEMANAL')
    cnxn.commit()
    cursor.close()
print('foi')


# In[ ]:






# In[47]:





# In[48]:


print(concurso)


# In[ ]:




