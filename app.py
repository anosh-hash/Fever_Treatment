import streamlit as st
import pandas as pd
import os

st.title("🩺 Fever Treatment Recommendation System")

file_name = "enhanced_fever_medicine_recommendation_.xlsx"

if not os.path.exists(file_name):
    st.error("Dataset file not found!")
    st.stop()

df = pd.read_excel(file_name)

st.header("Enter Patient Details")

age = st.number_input("Age", min_value=0, max_value=120)
temperature = st.number_input("Temperature (°F)", step=0.1)
bmi = st.number_input("BMI", step=0.1)

headache = st.selectbox("Headache?", ["Yes", "No"])
body_ache = st.selectbox("Body Ache?", ["Yes", "No"])
fatigue = st.selectbox("Fatigue?", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
allergies = st.selectbox("Allergies?", ["Yes", "No"])
diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-vegetarian","Vegan"])
pregnancy = st.selectbox("Pregnant?", ["Yes", "No"])
previous_med = st.text_input("Previous Medication")

if st.button("Get Recommendation"):

    filtered = df[
        (df["Age"].between(age - 5, age + 5)) &
        (df["Temperature"].between(temperature - 0.5, temperature + 0.5)) &
        (df["BMI"].between(bmi - 2.0, bmi + 2.0)) &
        (df["Headache"] == headache) &
        (df["Body_Ache"] == body_ache) &
        (df["Fatigue"] == fatigue) &
        (df["Gender"] == gender) &
        (df["Allergies"] == allergies) &
        (df["Diet_Type"] == diet_type) &
        (df["Pregnancy"] == pregnancy)
    ]

    if filtered.empty:
        st.warning("No similar patient data found. Please consult a doctor.")
    else:
        suggestion = filtered["Recommended_Medication"].mode()[0]

        if pregnancy == "Yes" and suggestion.lower() == "ibuprofen":
            st.error("Ibuprofen not recommended during pregnancy.")
        else:
            st.success(f"Recommended Treatment: {suggestion}")
