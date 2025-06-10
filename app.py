import streamlit as st
import pandas as pd
import joblib

# Load model and column structure
model = joblib.load("ap_outage_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

st.title("⚡ Andhra Pradesh Electricity Outage Predictor")

towns = ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Tirupati', 'Kurnool',
         'Rajahmundry', 'Kadapa', 'Anantapur', 'Ongole', 'Eluru', 'Chittoor',
         'Tenali', 'Adoni', 'Hindupur', 'Srikakulam', 'Vizianagaram', 'Nandyal',
         'Machilipatnam', 'Narasaraopet', 'Tadepalligudem', 'Bhimavaram',
         'Gudivada', 'Guntakal', 'Proddatur', 'Dharmavaram', 'Madanapalle',
         'Mangalagiri', 'Tadpatri', 'Markapuram', 'Amalapuram']

month = st.selectbox("Month", ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
day = st.selectbox("Day of Week", ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
town = st.selectbox("Town", towns)

temp = st.slider("Temperature (°C)", 28.0, 45.0, 35.0)
rain = st.slider("Rainfall (mm)", 0.0, 300.0, 50.0)
load = st.slider("Electricity Load (MW)", 800.0, 2500.0, 1500.0)

if st.button("Predict Outage"):
    input_dict = {col: 0 for col in feature_columns}
    input_dict['temperature'] = temp
    input_dict['rainfall_mm'] = rain
    input_dict['load_MW'] = load

    # One-hot encoding for town, month, day
    town_col = f"town_{town}"
    month_col = f"month_{month}"
    day_col = f"day_of_week_{day}"

    if town_col in input_dict:
        input_dict[town_col] = 1
    if month_col in input_dict:
        input_dict[month_col] = 1
    if day_col in input_dict:
        input_dict[day_col] = 1

    input_df = pd.DataFrame([input_dict])

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠️ Electricity Outage Predicted")
    else:
        st.success("✅ No Outage Expected")
