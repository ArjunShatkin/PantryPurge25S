import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.write("# Update Issue")



issues = requests.put('http://api:4000/i/issues').json()
try:
  st.dataframe(issues)
except:
  st.write("could not connect to databade to get users!")

# add a place to enter the updated information 

