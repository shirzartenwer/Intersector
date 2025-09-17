from Core.two_collection_intersector import TwoCollectionIntersector
from config import MIN_COLLECTION_SIZE, MAX_COLLECTION_SIZE
import streamlit as st

# --- Streamlit app ---
st.title("Welcome to the Intersector!")
st.write("This app gives you a simple interface to intersect two sets of numbers.")

# --- Define the two collections and their sizes ---
st.write("Please define the two collections you want to intersect:")
collection_names = ["Collection A", "Collection B"]
size_a = st.number_input(f"Size of {collection_names[0]}:", min_value=MIN_COLLECTION_SIZE, max_value=MAX_COLLECTION_SIZE, value=50)
size_b = st.number_input(f"Size of {collection_names[1]}:", min_value=MIN_COLLECTION_SIZE, max_value=MAX_COLLECTION_SIZE, value=25)

st.write("To have a performant experience, while calculating the intersection, one collection will be put into a hashset.")

# --- Use a form so the submit happens in one go ---

with st.form("choice_form", clear_on_submit=False):
    choice = st.radio(
        "Choose one:",
        collection_names,
        index=None,  # start with nothing selected
        horizontal=True,
        key="choice_given"
    )
    submitted = st.form_submit_button("Run Intersection", key="run_button")

if submitted:
    if choice is None:
        st.warning("Please choose an option before submitting.")
    else:
        # Create intersector with current sizes to avoid stale data
        intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
        st.success(f"You chose: **{choice}**")
        result, execution_time = intersector.intersect_legacy(0 if choice == collection_names[0] else 1)
        st.info(f"The size of the intersection is: {len(result)}")
        st.info(f"The runtime of intersection was: {execution_time}")
