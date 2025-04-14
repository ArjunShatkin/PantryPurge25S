
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Casual Cook Home")
st.write("Welcome to the Casual Cook Home Page!")

st.header("Features")
st.write("Search for Recipes")
st.write("Review History")
st.write("Recommendations")

if st.button("Search for Recipes"):
    st.switch_page("search_recipes.py")
if st.button("Review History"):
    st.write("Review History is not implemented yet.")
if st.button("Recommendations"):
    st.write("Recommendations is not implemented yet.")