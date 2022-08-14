import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl

servico = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('window-size=400,800')

user = input('digite o produto desejado: ')

url = 'https://www.mercadolivre.com.br'
navegador = webdriver.Chrome(options=options, service=servico)
navegador.get(url)
sleep(2)

imput_place = navegador.find_element(By.XPATH, '//*[@id="cb1-edit"]')
imput_place.send_keys(user)
imput_place.submit()
sleep(5)

page_content =  navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')
dados = []
hospedagens = site.findAll('div', attrs={'class': 'ui-search-result__content-wrapper'})

for hospedagem in hospedagens:

    hospedagem_des = hospedagem.find('h2', attrs={'class': 'ui-search-item__title'})
    hospedagem_preco = hospedagem.find('span', attrs={'class':'price-tag-fraction'})
    hospedagem_url = hospedagem.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})

    hospedagem_des = hospedagem_des.text
    hospedagem_preco =  hospedagem_preco.text
    hospedagem_url = hospedagem_url['href']

    print('')

    dados.append([hospedagem_des, hospedagem_preco, hospedagem_url])


dataf = pd.DataFrame(dados, columns=['Produto', 'Preco', 'URL'])
dataf.to_excel('produtos.xlsx', index=False)