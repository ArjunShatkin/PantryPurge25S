import streamlit as st
import requests
from datetime import datetime

with st.form("New Issue"):
  chef_id = st.text_input("Chef ID")
  recipe_id = st.text_input("Recipe ID")
  sub_status = st.selectbox("Submission Status", ["Not Submitted", "Submitted"], index=0)
  submission = st.form_submit_button("Submit Recipe")

if submission:
    data = {}
    data['RecipeID'] = recipe_id
    data['ChefID'] = chef_id
    data ['SubStatus'] = sub_status

    st.write(data)

    response = requests.post(f'http://api:4000/r/recipes/{int(recipe_id)}/newsletter', json=data)
    
    if response.status_code == 200:
            st.success(f"Successfully deleted recipe with ID {recipe_id}.")
    else:
        st.error(f"Failed to submit newsletter. Status code: {response.status_code}")
        st.json(response.json())