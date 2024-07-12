import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

option = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))

if option == "Predict":
    show_predict_page()
else:
    # st.write("Explore functionality is not implemented yet.")
    show_explore_page()