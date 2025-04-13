import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import requests
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('System Issues')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

if st.button('Update Issue', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/update_issue.py')


users = requests.get('http://api:4000/i/issues').json()
try:
  st.dataframe(users)
except:
  st.write("could not connect to databade to get users!")

