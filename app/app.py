import streamlit as st
import joblib
import pandas as pd

model = joblib.load('delivery_model.pkl')

st.title("Food Delivery Time Prediction")

age = st.number_input("Age")
rating = st.number_input("Rating")
distance = st.number_input("Distance")

vehicle = st.selectbox("Vehicle", ["motorcycle", "scooter"])
order = st.selectbox("Order", ["Snack", "Drinks", "Buffet"])

# IMPORTANT PART 🔥
input_df = pd.DataFrame(columns=model.feature_names_in_)
input_df.loc[0] = 0

input_df['delivery_person_age'] = age
input_df['delivery_person_ratings'] = rating
input_df['distance'] = distance

# category mapping
if f"type_of_vehicle_{vehicle}" in input_df.columns:
    input_df[f"type_of_vehicle_{vehicle}"] = 1

if f"type_of_order_{order}" in input_df.columns:
    input_df[f"type_of_order_{order}"] = 1

if st.button("Predict"):
    pred = model.predict(input_df)
    st.success(f"Delivery Time: {pred[0]:.2f} minutes")