import streamlit as st
import pandas as pd
import os
import urllib.parse

# ---------------------------
# Sample Medicine Dataset
# ---------------------------

data = {
    "Min_Temp": [100, 102],
    "Max_Temp": [101.9, 104],
    "Recommended_Medication": ["Paracetamol", "Ibuprofen"]
}

medicine_df = pd.DataFrame(data)

# ---------------------------
# App Title
# ---------------------------

st.title("🩺 Fever Treatment Recommendation System")
st.header("Enter Patient Details")

# ---------------------------
# User Inputs
# ---------------------------

age = st.number_input("Age", min_value=0, max_value=120)
temperature = st.number_input("Temperature (°F)", step=0.1)

# ---------------------------
# BMI Calculator
# ---------------------------

st.subheader("BMI Calculator")

height_cm = st.number_input("Enter your height (in cm)", min_value=0.0)
weight = st.number_input("Enter your weight (in kg)", min_value=0.0)

bmi = 0

if height_cm > 0 and weight > 0:
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    st.success(f"Your BMI is: {round(bmi,2)}")

# ---------------------------
# Additional Details
# ---------------------------

gender = st.selectbox("Gender", ["Male", "Female", "Other"])
headache = st.checkbox("Headache?")
body_ache = st.checkbox("Body Ache?")
fatigue = st.checkbox("Fatigue?")
allergies = st.text_input("Allergies?")
diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])

pregnant = "No"
if gender == "Female":
    pregnant = st.selectbox("Pregnant?", ["No", "Yes"])

previous_med = st.text_input("Previous Medication (if any)")

# ---------------------------
# Recommendation Button
# ---------------------------

if st.button("Get Recommendation"):

    if temperature < 100:
        st.success("✅ No fever detected. Stay hydrated and rest.")
    
    else:
        st.error("🌡 Fever Detected!")

        try:
            # Find medicine based on temperature
            filtered = medicine_df[
                (medicine_df["Min_Temp"] <= temperature) &
                (medicine_df["Max_Temp"] >= temperature)
            ]

            if not filtered.empty:

                suggested_med = filtered["Recommended_Medication"].mode()[0]

                # If previous medicine given
                if previous_med:

                    if previous_med.lower() == suggested_med.lower():
                        # Suggest alternative
                        alt = medicine_df[
                            medicine_df["Recommended_Medication"].str.lower() != previous_med.lower()
                        ]

                        if not alt.empty:
                            alternative_med = alt["Recommended_Medication"].mode()[0]
                            st.warning(f"⚠ Previous medicine ineffective.")
                            st.success(f"💊 Suggested Alternative: {alternative_med}")
                        else:
                            st.error("Doctor consultation needed.")
                    else:
                        st.success(f"💊 Recommended Treatment: {suggested_med}")

                else:
                    st.success(f"💊 Recommended Treatment: {suggested_med}")

            else:
                st.warning("No matching medicine found. Please consult doctor.")

        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ---------------------------
# Save Patient History
# ---------------------------

file_name = "health_history.csv"

if st.button("Save Record"):

    new_data = {
        "Age": age,
        "Temperature": temperature,
        "BMI": round(bmi, 2),
        "Gender": gender,
        "Headache": headache,
        "Body Ache": body_ache,
        "Fatigue": fatigue,
        "Allergies": allergies,
        "Diet": diet,
        "Pregnant": pregnant,
        "Previous Medication": previous_med
    }

    if os.path.exists(file_name):
        old_df = pd.read_csv(file_name)
        updated_df = pd.concat([old_df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        updated_df = pd.DataFrame([new_data])

    updated_df.to_csv(file_name, index=False)
    st.success("✅ Record Saved Successfully!")

# ---------------------------
# Show History
# ---------------------------

if os.path.exists(file_name):
    st.subheader("Previous Health Records")
    history_df = pd.read_csv(file_name)
    st.dataframe(history_df)

# ---------------------------
# Hospital Finder
# ---------------------------

st.markdown("---")
st.subheader("🏥 Hospital Finder")

location = st.text_input("Enter your area / city")

if st.button("Find Nearby Hospital"):

    if location.strip() == "":
        st.warning("Please enter your location.")
    else:
        query = urllib.parse.quote(f"hospitals near {location}")
        maps_url = f"https://www.google.com/maps/search/{query}"
        st.markdown(f"[Click here to view hospitals near you]({maps_url})")