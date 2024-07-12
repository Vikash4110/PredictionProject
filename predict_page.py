import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_Country = data["le_Country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""##### We need some information to predict the salary""")

    # Print the classes of the label encoders for debugging
#     st.write(f"Country classes: {le_Country.classes_}")
#     st.write(f"Education classes: {le_education.classes_}")

    countries = (
       "United States",      
"India",             
"United Kingdom",
"Germany" ,          
"Canada",             
"Brazil",             
"France",            
"Spain",            
"Australia",           
"Netherlands",      
"Poland",             
"Italy",             
"Russian Federation",  
"Sweden",
    )

    education = (
     "Less than a Bachelors",
     "Bachelor’s degree",
     "Master’s degree",
     "Post grad",
    )

    country = st.selectbox("Country", countries)
    education_level = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")

    if ok:
        X = np.array([[country, education_level, experience]])
        X[:, 0] = le_Country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")