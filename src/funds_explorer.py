import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

colunasFundo = ['Codigo', 'Nome', 'Preco', 'VolumeMedio', 'DividendYield', 'PatrimonioLiq', 'P/VP', 'Cotas', 'Segmento']
dfFundos = pd.DataFrame(columns=colunasFundo)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
request_url = "https://www.fundsexplorer.com.br/funds"
request = Request(url=request_url, headers=headers)

html = urlopen(request)
res = BeautifulSoup(html.read(),"html5lib")
tags = res.find_all("span", {"class":"symbol"})

print("------------------------------")
print("Initializing data gathering...")

for tag in tags:
    fii = tag.getText()

    print("Gathering {}".format(fii))

    request_url = "https://www.fundsexplorer.com.br/funds/" + fii
    request = Request(url=request_url, headers=headers)
    html = urlopen(request)
    res = BeautifulSoup(html.read(),"html5lib")

    Codigo = tag.getText()
    Nome = res.find_all("h3", {"class":"section-subtitle"})[0].getText()
    Preco = res.find_all("span", {"class":"price"})[0].getText().split("\n")[1].strip()
    VolumeMedio = res.find_all("span", {"class":"indicator-value"})[0].getText().split("\n")[1].strip()
    DividendYield = res.find_all("span", {"class":"indicator-value"})[3].getText().split("\n")[1].strip()
    PatrimonioLiq = res.find_all("span", {"class":"indicator-value"})[4].getText().split("\n")[1].strip()
    PVP = res.find_all("span", {"class":"indicator-value"})[6].getText().split("\n")[1].strip()
    Cotas = res.find("span", {"class":"title"}, text="Cotas emitidas").find_all_next("span")[0].getText().split("\n")[1].strip()
    Segmento = res.find("span", {"class":"title"}, text="Segmento").find_all_next("span")[0].getText().split("\n")[1].strip()

    linhasFundo = [Codigo, Nome, Preco, VolumeMedio, DividendYield, PatrimonioLiq, PVP, Cotas, Segmento]

    dfFundos.loc[Codigo] = linhasFundo

indNA = dfFundos["VolumeMedio"] != 'N/A'
indZero = dfFundos["VolumeMedio"] != '0'

dfFundos = dfFundos[indNA]
dfFundos = dfFundos[indZero]

dfFundos.to_csv("fundos.csv", sep = ";", encoding = 'utf-8-sig')

dfFundos['Segmento'].describe()
dfFundos['Segmento'].unique()

dfFundos.describe()

print("Data gathering successful!")
print("------------------------------")
