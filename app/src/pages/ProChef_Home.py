import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Welcome Professional Chef, Anthony")
st.write("Welcome to the Professional Chef Home Page!")

if st.button("View Your Recipes"):
    st.switch_page("pages/100_ViewRecipes.py")

if st.button("Add A Recipe"):
    st.switch_page("pages/101_AddRecipe.py")

if st.button("Update A Recipe"):
    st.switch_page("pages/search_recipes.py")

if st.button("View Nearby Chefs"):
    st.switch_page("pages/search_recipes.py")



