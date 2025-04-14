
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Casual Cook Home")
st.write("Welcome to the Casual Cook Home Page!")

st.header("Features")
if st.button("Search for Recipes"):
    st.switch_page("pages/search_recipes.py")