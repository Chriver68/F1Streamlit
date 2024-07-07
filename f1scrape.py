import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re
import plotly
import plotly.express as px
from datetime import datetime


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
            'Grandprix': gp_name.capitalize(),
            'soort_race': soort_race.capitalize(),
            'position': driver.find('td', class_="dark").text,
            'nr': driver.find('td', class_='dark hide-for-mobile').text,
            'Driver': driver.find('span', class_='uppercase hide-for-desktop').text,
            'name': driver.find('span', class_='hide-for-tablet').text + ' ' + driver.find('span', class_='hide-for-mobile').text,
            'team': driver.find('td', class_="semi-bold uppercase hide-for-tablet").text,
            'Points': int(driver.find_all('td', class_='bold')[3].text),}

    gegevens.append(data)

df = pd.DataFrame(gegevens)

df2 = df[['Driver', 'Points']]
df2.sort_values(by=['Points'])
punten_cumulatief = df2.groupby(['Driver']).sum().reset_index()
punten_cumulatief = punten_cumulatief.sort_values(by='Points', ascending = False)

fig = px.bar(punten_cumulatief, x='Driver', y = 'Points', text= 'Points', color='Driver')
fig = fig.update_layout(autosize=False, width = 800, height=800, bargap=0.0,bargroupgap=0.0)

#punten_cumulatief['Ranking']= punten_cumulatief['Points'].rank(ascending=False)
punten_cumulatief.insert(0, 'Ranking', punten_cumulatief['Points'].rank(ascending=False))


df['Grouped Cumulative Sum'] = df[['Driver', 'Points']].groupby('Driver').cumsum()
df['date'] = pd.to_datetime(df['date'])
most_recent_date = df['date'].max()
most_recent_race = df[df['date'] == most_recent_date].Grandprix.max()
most_recent_date = datetime.fromtimestamp(most_recent_date.timestamp())

