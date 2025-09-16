from Core.two_collection_intersector import TwoCollectionIntersector
import streamlit as st
import random

# --- Streamlit app ---
st.title("Wecome to the Intersector!")
st.write("This app gives you a simple interface to intersect two set of numbers.")

size_a = st.number_input("Size of collection A:", min_value=0, max_value=1000000, value=50)
size_b = st.number_input("Size of collection B:", min_value=0, max_value=1000000, value=25)

# Generate random collections based on user input
collection_a = [random.random() for _ in range(size_a)]
collection_b = [random.random() for _ in range(size_b)]
intersector = TwoCollectionIntersector(collection_a, collection_b)

st.write("To have a performant experience, while calculaing the intersection, one collection will be put into a hashset.")

# --- Use a form so the submit happens in one go ---
with st.form("choice_form", clear_on_submit=False):
    choice = st.radio(
        "Choose one:",
        ["Collection A", "Collection B"],
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
        result, run_time = intersector.intersect(choice)
        st.info(f"The size of the intersection is: {len(result)}")
        st.info(f"The runtime of intersection was: {run_time}")
