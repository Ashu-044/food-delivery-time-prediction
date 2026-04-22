import streamlit as st
import joblib
import pandas as pd
import gdown
import os

# Download model (if not exists)

def download_model():
    if not os.path.exists("delivery_model.pkl"):
        url = "https://drive.google.com/uc?id=173twUbt2exwrNfRjxHtD4AT1a5R16JoX"
        gdown.download(url, "delivery_model.pkl", quiet=True)


# Load model (cached)

@st.cache_resource
def load_model():
    download_model()
    return joblib.load("delivery_model.pkl")

model = load_model()


# UI

st.title("🚚 Food Delivery Time Prediction")

st.caption("⚠️ Enter realistic values → Age: 18–60, Rating: 1–5, Distance: 0–50 km")

age = st.number_input("Age", min_value=18, max_value=60, value=30)
rating = st.number_input("Rating", min_value=1.0, max_value=5.0, value=4.0)
distance = st.number_input("Distance (km)", min_value=0.0, max_value=50.0, value=10.0)

vehicle = st.selectbox("Vehicle", ["motorcycle", "scooter"])
order = st.selectbox("Order", ["Snack", "Drinks", "Buffet"])


# Prediction

if st.button("Predict"):

    # Extra safety validation
    if distance > 50:
        st.error("❌ Distance too large. Please enter value below 50 km.")
        st.stop()

    # Create input dataframe
    input_df = pd.DataFrame(columns=model.feature_names_in_)
    input_df.loc[0] = 0

    input_df['delivery_person_age'] = age
    input_df['delivery_person_ratings'] = rating
    input_df['distance'] = distance

    # One-hot encoding match
    vehicle_col = f"type_of_vehicle_{vehicle}"
    order_col = f"type_of_order_{order}"

    if vehicle_col in input_df.columns:
        input_df[vehicle_col] = 1

    if order_col in input_df.columns:
        input_df[order_col] = 1

    # Predict
    pred = model.predict(input_df)

    # Output
    st.success(f"⏱️ Estimated Delivery Time: {pred[0]:.2f} minutes")

    # Info message
    st.info("💡 Prediction is reliable within realistic delivery range (0–50 km).")