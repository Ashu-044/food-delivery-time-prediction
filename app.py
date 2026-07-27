import streamlit as st
import joblib
import pandas as pd
import gdown
import os

st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

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

st.markdown("""
<div class="hero">

<div class="hero-title">
🚚 Food Delivery Time Prediction
</div>

<div class="hero-subtitle">
AI-Powered Delivery Time Estimator
</div>

<div class="hero-text">
Predict food delivery time using Machine Learning and Random Forest Regression.
</div>

</div>
""", unsafe_allow_html=True)

# age = st.number_input("Age", min_value=18, max_value=60, value=30)
# rating = st.number_input("Rating", min_value=1.0, max_value=5.0, value=4.0)
# distance = st.number_input("Distance (km)", min_value=0.0, max_value=50.0, value=10.0)

# vehicle = st.selectbox("Vehicle", ["motorcycle", "scooter"])
# order = st.selectbox("Order", ["Snack", "Drinks", "Buffet"])

left, right = st.columns([1.25, 0.75])

with left:

    #st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">👤 Delivery Partner</div>',
        unsafe_allow_html=True
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=60,
        value=30
    )

    rating = st.number_input(
        "Rating",
        min_value=1.0,
        max_value=5.0,
        value=4.0
    )

    st.divider()

    st.markdown(
        '<div class="section-title">📦 Delivery Details</div>',
        unsafe_allow_html=True
    )

    #st.markdown("</div>", unsafe_allow_html=True)

    distance = st.number_input(
        "Distance (km)",
        min_value=0.0,
        max_value=50.0,
        value=10.0
    )

    vehicle = st.selectbox(
        "Vehicle",
        ["motorcycle","scooter"]
    )

    order = st.selectbox(
        "Order",
        ["Snack","Drinks","Buffet"]
    )

    predict = st.button(
        "🚀 Predict Delivery Time",
        use_container_width=True
    )

    #st.markdown("</div>", unsafe_allow_html=True)

with right:

    #container = st.container(border=True)

    #with container:
        st.markdown(
            '<div class="section-title">📊 Prediction</div>',
            unsafe_allow_html=True
        )

        prediction_box = st.empty()


# st.markdown("</div>", unsafe_allow_html=True)



# Prediction

if predict:

    # Extra safety validation
    if distance > 50:
        st.error("❌ Distance too large. Please enter value below 50 km.")
        st.stop()

    # Create input dataframe
    input_df = pd.DataFrame(columns=model.feature_names_in_)
    input_df.loc[0] = 0

    input_df["delivery_person_age"] = age
    input_df["delivery_person_ratings"] = rating
    input_df["distance"] = distance

    vehicle_col = f"type_of_vehicle_{vehicle}"
    order_col = f"type_of_order_{order}"

    if vehicle_col in input_df.columns:
        input_df[vehicle_col] = 1

    if order_col in input_df.columns:
        input_df[order_col] = 1

    pred = model.predict(input_df)

    if pred[0] < 20:
        status = "🟢 Fast Delivery"
        css = "fast" 

    elif pred[0] < 35:
         status = "🟡 Normal Delivery"
         css = "normal"

    else:
        status = "🔴 Delayed Delivery"
        css = "delayed"

    prediction_box.markdown(
        f"""
    <div class="result-card">

    <h1 class="result-time">{pred[0]:.1f} min</h1>

    <p class="result-label">
    Estimated Delivery Time
    </p>

    <span class="result-status {css}">
    {status}
    </span>

    <p style="color:#94A3B8; margin-top:20px;">
        Prediction generated using the
        <b>Random Forest Regression</b> model.
    </p>

    </div>
    """,
        unsafe_allow_html=True,
    )


