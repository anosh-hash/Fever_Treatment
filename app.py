import streamlit as st
import pandas as pd
import os
import urllib.parse

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="உயிர் தோழன்",
    page_icon="🩺",
    layout="wide"
)

# -------------------------------------------------
# MEDICAL THEME CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f4f8fb;
}

section[data-testid="stSidebar"] {
    background-color: #0e1a2b;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

div.stButton > button {
    background-color: #0077b6;
    color: white;
    border-radius: 10px;
    font-weight: bold;
    height: 3em;
    width: 100%;
}

.success-box {
    background-color: #2e7d32;
    padding: 15px;
    border-radius: 10px;
    color: white;
}

.warning-box {
    background-color: #f9a825;
    padding: 15px;
    border-radius: 10px;
    color: black;
}

.error-box {
    background-color: #d32f2f;
    padding: 15px;
    border-radius: 10px;
    color: white;
}

.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SAMPLE MEDICINE DATA
# -------------------------------------------------
data = {
    "Min_Temp": [100, 102],
    "Max_Temp": [101.9, 104],
    "Recommended_Medication": ["Paracetamol", "Ibuprofen"]
}
medicine_df = pd.DataFrame(data)

# -------------------------------------------------
# SIDEBAR ONLY DESIGN
# -------------------------------------------------
st.sidebar.title("🩺 Patient Details")

age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)

temperature = st.sidebar.number_input(
    "Temperature (°F)",
    min_value=90.0,
    max_value=110.0,
    value=98.6
)

gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

st.sidebar.subheader("Symptoms")

headache = st.sidebar.checkbox("Headache")
body_ache = st.sidebar.checkbox("Body Ache")
fatigue = st.sidebar.checkbox("Fatigue")

allergies = st.sidebar.text_input("Allergies (if any)")
diet = st.sidebar.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])

pregnant = "No"
if gender == "Female":
    pregnant = st.sidebar.selectbox("Pregnant", ["No", "Yes"])

previous_med = st.sidebar.text_input("Previous Medication")

# -------------------------------------------------
# BMI SECTION
# -------------------------------------------------
st.sidebar.subheader("BMI Calculator")

height_cm = st.sidebar.number_input("Height (cm)", min_value=0.0)
weight = st.sidebar.number_input("Weight (kg)", min_value=0.0)

bmi = 0
if height_cm > 0 and weight > 0:
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    st.sidebar.success(f"BMI: {round(bmi,2)}")

# -------------------------------------------------
# MAIN DASHBOARD AREA
# -------------------------------------------------
st.title("🏥 உயிர் தோழன்")

st.markdown("### 🧠 Diagnosis & Recommendation")

if st.button("Analyze Patient Condition"):

    if temperature < 99:
        st.markdown("""
        <div class="success-box">
        ✅ No significant fever detected.
        </div>
        """, unsafe_allow_html=True)

    else:

        filtered = medicine_df[
            (medicine_df["Min_Temp"] <= temperature) &
            (medicine_df["Max_Temp"] >= temperature)
        ]

        if not filtered.empty:

            suggestion = filtered["Recommended_Medication"].mode()[0]

            if previous_med:
                alt = medicine_df[
                    medicine_df["Recommended_Medication"].str.lower() != previous_med.lower()
                ]

                if not alt.empty:
                    alt_suggestion = alt["Recommended_Medication"].mode()[0]

                    if alt_suggestion.lower() == previous_med.lower():
                        st.markdown("""
                        <div class="error-box">
                        ⚠ Previous medicine ineffective. Consult doctor immediately.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="warning-box">
                        💊 Suggested Alternative Treatment: {alt_suggestion}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-box">
                    Doctor consultation required.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                <h3>💊 Recommended Medicine</h3>
                <h2 style='color:#0077b6;'>{suggestion}</h2>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="error-box">
            🚨 High Fever! Immediate medical attention required.
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------
# SAVE PATIENT HISTORY
# -------------------------------------------------
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

# -------------------------------------------------
# SHOW HISTORY
# -------------------------------------------------
if os.path.exists(file_name):
    st.subheader("📁 Previous Health Records")
    history_df = pd.read_csv(file_name)
    st.dataframe(history_df)

# -------------------------------------------------
# HOSPITAL FINDER
# -------------------------------------------------
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

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.markdown("© 2026 Fever Treatment Professional Dashboard | Built with Streamlit")
