
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Search for Recipes")
st.write("Enter the ingredients you have on hand (comma-separated):")
st.write("You may also filter recipes (all fields must have a value)")

columns = st.columns(2)

ingredients_column = columns[0]
ingredients_input = ingredients_column.text_input("Ingredients", "chicken, rice, broccoli")

filter_column = columns[1]
max_prep_time = filter_column.number_input("Max Preparation Time (minutes)", min_value=0, value=360)
cuisine = filter_column.text_input("Cuisine", "Italian")
diet = filter_column.text_input("Diet", "Vegetarian")

if st.button("Search"):
    ingredients_results = []
    filter_results = []

    if ingredients_input.strip():
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
        ingredients_url = "http://api:4000/casual_cooks/recipes/match"
        ingredients_response = requests.post(ingredients_url, json={
            "ingredients": ingredients})
        if ingredients_response.status_code == 200:
            ingredients_results = ingredients_response.json()

    used_filter = max_prep_time > 0 and cuisine.strip() and diet.strip()

    if used_filter:
        filters = {
            "max_prep_time": max_prep_time,
            "cuisine": cuisine.strip(),
            "diet": diet.strip()
        }
        filter_url = "http://api:4000/casual_cooks/recipes/filter"
        filter_response = requests.get(filter_url, params=filters)
        if filter_response.status_code == 200:
            filter_results = filter_response.json()

    search_results = []
    if used_filter:
        search_results = [recipe for recipe in ingredients_results if recipe in filter_results]
    else:
        search_results = ingredients_results

    if search_results:
        st.write("Search Results:")
        for recipe in search_results:
            st.write(f"- {recipe['name']}")
            st.write(f"  Ingredients: {', '.join(recipe['ingredients'])}")
            st.write(f"  Instructions: {recipe['instructions']}")
    else:
        st.write("No recipes in database.")