import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re
import football
import f1
import contact
from f1scrape import *
from streamlit_option_menu import option_menu

st.set_page_config(page_title='F1 2024 Dashboard',
                   page_icon='bar_chart',
                   layout='wide')

class MultiApp:

    def __init__(self):
        self.apps=[]

    def add_app(self, title, function):
        self.apps.append({
            'title': title,
            'function': function,
        })

    def run():
        app = option_menu(None, ["F1", "Eredivisie", 'Contact'],
                           menu_icon="cast",default_index=0, orientation="horizontal")
        if app =='Eredivisie':
            football.app()
        if app == 'F1':
            f1.app()
        if app =='Contact':
            contact.app()

    run()