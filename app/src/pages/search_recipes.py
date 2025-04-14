
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Search for Recipes")
st.write("Enter the ingredients you have on hand (comma-separated):")

columns = st.columns(2)

ingredients_column = columns[0]
ingredients_input = ingredients_column.text_input("Ingredients", "chicken, rice, broccoli")

filter_column = columns[1]
prep_time_max = filter_column.number_input("Max Preparation Time (minutes)", min_value=0, value=360)
cuisine = filter_column.text_input("Cuisine", "")
diet_rest = filter_column.text_input("Diet", "")

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

    used_filters = {}
    if prep_time_max > 0:
        used_filters["prep_time_max"] = prep_time_max
    if cuisine:
        used_filters["cuisine"] = cuisine.strip()
    if diet_rest:
        used_filters["diet_rest"] = diet_rest.strip()

    if used_filters:
        filter_url = "http://api:4000/casual_cooks/recipes/filter"
        filter_response = requests.get(filter_url, params=used_filters)
        if filter_response.status_code == 200:
            filter_results = filter_response.json()

    if ingredients_results and not filter_results:
        found_ids = {recipe['RecipeID'] for recipe in filter_results}
        search_results = [recipe for recipe in ingredients_results if recipe['RecipeID'] in found_ids]
    else:
        search_results = ingredients_results

    if search_results:
        st.write("Search Results:")
        for recipe in search_results:
            st.write(f"- {recipe['RecipeName']}")
            st.write(f"  Description: {recipe['Description']}")
    else:
        st.write("No recipes in database.")