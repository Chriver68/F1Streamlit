import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import plotly.express as px
from datetime import datetime
import numpy as np

def app():
    st.write('')

    url = "https://www.knvb.nl/competities/eredivisie/uitslagen"
    response = requests.get(url)

    if response.status_code == 200:
        # De aanvraag was succesvol, ga verder met het parsen van de HTML
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    else:
        print("Fout bij het ophalen van de pagina.")

    eredivisie_soup = soup.select('div.table-wrapper')
    resultaten = []
    for item in eredivisie_soup:
        date = item.select_one('span.title').text

        datum1 = date.split()

        if datum1[1] == 'januari':
            datum1[1] = '01'
        if datum1[1] == 'februari':
            datum1[1] = '02'
        if datum1[1] == 'maart':
            datum1[1] = '03'
        if datum1[1] == 'april':
            datum1[1] = '04'
        if datum1[1] == 'mei':
            datum1[1] = '05'
        if datum1[1] == 'juni':
            datum1[1] = '06'
        if datum1[1] == 'juli':
            datum1[1] = '07'
        if datum1[1] == 'augustus':
            datum1[1] = '08'
        if datum1[1] == 'september':
            datum1[1] = '09'
        if datum1[1] == 'oktober':
            datum1[1] = '10'
        if datum1[1] == 'november':
            datum1[1] = '11'
        if datum1[1] == 'december':
            datum1[1] = '12'

        datum = "-".join(datum1)

        date = datetime.strptime(datum, '%d-%m-%Y').date()

        wedstrijden = item.select('div.row')
        for wedstrijd in wedstrijden:

            if len(wedstrijd.select_one('div.value.center').text.split('-')) != 1:
                uitslag = wedstrijd.select_one('div.value.center').text
            else:
                uitslag = 'NaN'

            data = {
                'datum': date,
                'thuis': wedstrijd.select_one('div.value.home').text.strip().rstrip('*'),
                'uit': wedstrijd.select_one('div.value.away').text.strip().rstrip('*'),
                'uitslag': uitslag,
                'doelpunten_thuisploeg': wedstrijd.select_one('div.value.center').text.split('-')[0],
                'doelpunten_uitploeg': wedstrijd.select_one('div.value.center').text.split('-')[-1],
            }
            resultaten.append(data)

    resultaten = pd.DataFrame(resultaten)

    # verwijder gestaakte wedstrijden
    resultaten = resultaten.query('uitslag != "NaN"')

    resultaten[['doelpunten_thuisploeg', 'doelpunten_uitploeg']] = resultaten[
        ['doelpunten_thuisploeg', 'doelpunten_uitploeg']].astype(int)

    resultaten['saldo_uitslag'] = resultaten['doelpunten_thuisploeg'] - resultaten['doelpunten_uitploeg']

    conditions = [
        resultaten['saldo_uitslag'] == 0,
        resultaten['saldo_uitslag'] < 0,
        resultaten['saldo_uitslag'] > 0
    ]

    choices = ['1', '0', '3']
    choices2 = ['1', '3', '0']

    resultaten['punten_thuisploeg'] = np.select(conditions, choices, default='Unknown')
    resultaten['punten_uitploeg'] = np.select(conditions, choices2, default='Unknown')
    resultaten[['punten_thuisploeg', 'punten_uitploeg']] = resultaten[['punten_thuisploeg', 'punten_uitploeg']].astype(
        int)

    resultaten = resultaten.sort_values('datum', ascending=True)

    totaal1 = resultaten[['datum', 'thuis', 'punten_thuisploeg']]
    totaal2 = resultaten[['datum', 'uit', 'punten_uitploeg']]
    totaal1.rename(columns={'thuis': 'team', 'punten_thuisploeg': 'points'}, inplace=True)
    totaal2.rename(columns={'uit': 'team', 'punten_uitploeg': 'points'}, inplace=True)

    frames = [totaal1, totaal2]
    result = pd.concat(frames)
    result = result.sort_values(by=['team', 'datum'])
    result['grouped_points'] = result[['team', 'points']].groupby('team').cumsum().astype(int)

    totaal_punten = result.groupby('team').max().reset_index()
    totaal_punten = totaal_punten.sort_values(by=['grouped_points'], ascending=False)

    fig = px.bar(totaal_punten, x='team', y='grouped_points', text='team', color='team')
    fig = fig.update_layout(autosize=False, width=800, height=800, bargap=0.0, bargroupgap=0.0,
                            yaxis={'visible': True, 'showticklabels': True},
                            xaxis={'visible': True, 'showticklabels': False})

    fig2 = px.line(result, x='datum', y='grouped_points', color='team', text='grouped_points')
    fig2 = fig2.update_layout(yaxis={'visible': False, 'showticklabels': False},
                              autosize=False,
                              width=2000,
                              height=700, )

    col1, col2 = st.columns([1,3])
    col2.title('Season 2023/2024.')
    col1.write(fig)
    col2.write(fig2)