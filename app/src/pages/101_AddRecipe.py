import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Create A New Recipe Here")

st.write("# Create A Recipe")

with st.form("New Issue"):
  recipe_id = st.number_input("Input Recipe ID:", step=1)
  chef_id = st.number_input("Input Your Chef ID:", step=1)
  servings = st.selectbox("Enter the number of servings:",[i for i in range(20)])
  difficulty = st.selectbox("Enter the diffiulty level:",['Easy','Medium','Hard'])
  calories = st.number_input("Enter the number of Calories:", step=1)
  recipe_name = st.text_input("Name of Recipe:")
  description = st.text_area("Summarize the Recipe:")
  preptimemins = st.number_input("Enter the Prep Time in Minutes:", step=1)
  cooktimemins = st.number_input("Enter the Cook Time in Minutes:", step=1)
  video_url = st.text_input("Paste An Associated Video URL:")
  cuisine = st.text_input('Enter the Recipe Cuisine')
  submission = st.form_submit_button("Create Recipe")


  if submission:
    data = {}
    data['RecipeID'] = recipe_id
    data['ChefID'] = chef_id
    data ['Servings'] = servings
    data ['Difficulty'] = difficulty
    data ['Calories'] = calories
    data ['RecipeName'] = recipe_name
    data ['Description'] = description
    data ['PrepTimeMins'] = preptimemins
    data ['CookTimeMins'] = cooktimemins
    data ['VideoUrl'] = video_url
    data['Cuisine'] = cuisine

    st.write(data)

    response = requests.post('http://api:4000/r/recipes', json=data)

    if response.status_code == 200:
            st.success(f"Successfully submitted new recipe")
    else:
        st.error(f"Failed to submit new recipe. Status code: {response.status_code}")
