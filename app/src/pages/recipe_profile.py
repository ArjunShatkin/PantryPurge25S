
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()
st.title("Recipe Profile")

recipe_id = st.session_state["selected_id"]
profile_url = f"http://web-api-test:4000/cc/recipes/{recipe_id}/profile"
response = requests.get(profile_url)

if response.status_code == 200:
    data = response.json()

    st.header(data.get("RecipeName", "Recipe Details"))
    st.write("Difficulty:", data.get("Difficulty"))
    st.write("Cuisine:", data.get("Cuisine"))
    st.write("Servings:", data.get("Servings"))
    st.write("Calories:", data.get("Calories"))
    st.write("Prep Time (mins):", data.get("PrepTime"))
    st.write("Cook Time (mins):", data.get("CookTime"))
    st.write("Video URL:", data.get("VideoURL"))
    st.write("Number of Reviews:", data.get("NumReviews"))
    st.write("Number of Views:", data.get("NumViews"))
    st.write("Number of Shares:", data.get("NumShares"))
    st.write("Featured:", "Yes" if data.get("Featured") else "No")
    st.write("Published:", data.get("PublishDate"))
    st.write("Description:", data.get("Description"))

    st.subheader("Adjust Servings")
    new_servings = st.number_input("Enter your choice of servings.", min_value=1, value=data.get("Servings", 1))

    if st.button("Adjust Servings"):
        adjust_url = f"http://web-api-test:4000/cc/recipes/{recipe_id}/adjust_servings"
        response = requests.post(adjust_url, json={"new_servings": new_servings})
        adjusted_data = response.json()
        for ingedient in adjusted_data:
            st.write(f"- {ingedient['IngredientName']}: {ingedient['AdjustedQuantity']} {ingedient['MeasureUnit']}")

    st.subheader("Caloric Breakdown")
    calories = data.get("Calories")

    st.subheader("Reviews")
    reviews = data.get("Reviews")
    if reviews:
        for review in reviews:
            st.write(f"- {review['ReviewText']} (Rating: {review['Rating']})")
            st.write(f"- (Published: {review['PublishDate']})")
