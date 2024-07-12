import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def Shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[['Country', "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()

    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = Shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)

    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer's data")

    st.write(
        """ ### Stack Overflow Developer Survey """
    )

    data = df["Country"].value_counts().reset_index()
    data.columns = ['Country', 'Count']

    # Pie chart with Plotly
    fig1 = px.pie(data, names='Country', values='Count', title='Number of Data from Different Countries',
                  color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
    
    fig1.update_traces(textinfo='percent+label')

    st.plotly_chart(fig1)

    # Experience vs Salary interactive scatter plot
    fig2 = px.scatter(df, x='YearsCodePro', y='Salary', color='Country',
                      title='Years of Experience vs. Salary',
                      labels={'YearsCodePro': 'Years of Experience', 'Salary': 'Salary'},
                      hover_data=['EdLevel'])

    st.plotly_chart(fig2)

    # Salary distribution by Education Level
    fig3 = px.box(df, x='EdLevel', y='Salary', color='EdLevel', title='Salary Distribution by Education Level',
                  labels={'EdLevel': 'Education Level', 'Salary': 'Salary'})

    st.plotly_chart(fig3)

