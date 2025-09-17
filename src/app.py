from Core.two_collection_intersector import TwoCollectionIntersector
from config import MIN_COLLECTION_SIZE, MAX_COLLECTION_SIZE, RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX
import streamlit as st
import random

# --- Streamlit app ---
st.title("Welcome to the Intersector!")
st.write("This app gives you a simple interface to intersect two set of numbers.")

# --- Define the two collections and their sizes ---
st.write("Please define the two collections you want to intersect:")
name_of_two_collections = ["Collection A", "Collection B"]
size_a = st.number_input("Size of "+name_of_two_collections[0]+":", min_value=MIN_COLLECTION_SIZE, max_value=MAX_COLLECTION_SIZE, value=50)
size_b = st.number_input("Size of "+name_of_two_collections[1]+":", min_value=MIN_COLLECTION_SIZE, max_value=MAX_COLLECTION_SIZE, value=25)

# Generate random collections based on user input
collection_a = [random.randint(RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX) for _ in range(size_a)]
collection_b = [random.randint(RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX) for _ in range(size_b)]
intersector = TwoCollectionIntersector(collection_a, collection_b)

st.write("To have a performant experience, while calculaing the intersection, one collection will be put into a hashset.")

# --- Use a form so the submit happens in one go ---

with st.form("choice_form", clear_on_submit=False):
    choice = st.radio(
        "Choose one:",
        name_of_two_collections,
        index=None,  # start with nothing selected
        horizontal=True,
        key="choice_given"
    )
    submitted = st.form_submit_button("Run Intersection", key="run_button")

if submitted:
    if choice is None:
        st.warning("Please choose an option before submitting.")
    else:
        # Do whatever you want with `choice` here
        st.success(f"You chose: **{choice}**")
        result, run_time = intersector.intersect(0 if choice == name_of_two_collections[0] else 1)
        st.info(f"The size of the intersection is: {len(result)}")
        st.info(f"The runtime of intersection was: {run_time}")
