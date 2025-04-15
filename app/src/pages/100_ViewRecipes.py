import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Add sidebar links
SideBarLinks()

st.write("# Your Recipes")

# Input field for Chef ID
chef_id = st.text_input("Enter Chef ID", "")

# Function to fetch recipes based on Chef ID
def get_recipes_by_chef(chef_id):
    if chef_id:
        try:
            # Request to get recipes for the provided chef_id
            url = f'http://api:4000/r/chefs/{int(chef_id)}/recipes'
            response = requests.get(url)

            # Check if the response is successful
            if response.status_code == 200:
                recipes = response.json()
                st.write(f"Received recipes: {recipes}")
                # Convert recipes data to df
                df = pd.DataFrame(recipes)
                return df
            else:
                st.write(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
                return None
        except Exception as e:
            st.write(f"Error occurred: {str(e)}")
            return None
    else:
        st.write("Please enter a valid Chef ID.")
        return None

# Fetch and display recipes based on the input Chef ID
if chef_id:
    chef_recipes_df = get_recipes_by_chef(chef_id)
    if chef_recipes_df is not None:
        st.dataframe(chef_recipes_df)
else:
    st.write("Please enter a Chef ID to view their recipes.")
