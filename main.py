import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re


st.set_page_config(page_title='F1 2024 Dashboard',
                   page_icon='bar_chart',
                   layout='wide')
st.header('Test')

base_url  = 'https://www.formula1.com'
url = "https://www.formula1.com/en/results.html/2024/races.html"
response = requests.get(url)

if response.status_code == 200:
    # De aanvraag was succesvol, ga verder met het parsen van de HTML
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
else:
    print("Fout bij het ophalen van de pagina.")

#linkjes voor de grandprixs
linkjes = []
#linkjes voor de race en sprintrace
linkjes2 = []

urls_gp = soup.find_all('a', class_= 'dark bold ArchiveLink')

for url in urls_gp:
  linkje = base_url + url.get('href')
  linkjes.append(linkje)

gegevens = []

for linkje in linkjes:

  response = requests.get(linkje)

  if response.status_code == 200:
      # De aanvraag was succesvol, ga verder met het parsen van de HTML
      html = response.text
      soup = BeautifulSoup(html, "html.parser")
  else:
      print(f"Fout bij het ophalen van de pagina.{linkje}")

  quali = soup.find_all('li' ,class_="side-nav-item")
  quali1 = [a.find('a') for a in quali[1:]]

  extra = []
  [extra.append(item.get('href')) for item in quali1]

  [linkjes2.append(base_url+item) for item in extra if ((item.find('race-result')>=0) or (item.find('sprint-results')>0)) and (base_url + item)not in linkjes2 ]
  #linkjes2 = list(set(linkjes2))

for linkje in linkjes2:
  response = requests.get(linkje)
  if response.status_code == 200:
    # De aanvraag was succesvol, ga verder met het parsen van de HTML
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
  else:
    print(f"Fout bij het ophalen van de pagina.{linkje}")

  #naam van de race zelf ophalen
  x= linkje.find('/races')+12
  y = linkje.rfind('/')
  gp_name = linkje[x:y]

  a= linkje.find('html/')+5
  b = linkje.find('/races')
  gp_year =  linkje[a:b]

  #soort race
  x = linkje.rfind('/')
  y = linkje.find('-result')
  soort_race = linkje[x+1:y]

  drivers = soup.find_all('tr')[1:]
  #gegevens drivers ophalen
  for driver in drivers:
    data = {'year': gp_year,
            'date': soup.find('span', class_="full-date").text,
            'grandprix': gp_name,
            'soort_race': soort_race,
            'position': driver.find('td', class_="dark").text,
            'nr': driver.find('td', class_='dark hide-for-mobile').text,
            'code': driver.find('span', class_='uppercase hide-for-desktop').text,
            'name': driver.find('span', class_='hide-for-tablet').text + ' ' + driver.find('span', class_='hide-for-mobile').text,
            'team': driver.find('td', class_="semi-bold uppercase hide-for-tablet").text,
            'points': int(driver.find_all('td', class_='bold')[3].text),}

    gegevens.append(data)

df = pd.DataFrame(gegevens)
#st.dataframe(df)
print(df)