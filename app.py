import streamlit as st
import pandas as pd
import pickle
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import time

# Set page configuration
st.set_page_config(page_title="Seattle Weather Dashboard", page_icon="☁️", layout="centered", initial_sidebar_state="expanded")

# Weather icons mapping with user-friendly categories
WEATHER_CATEGORIES = {
    "rain": ("rainy", "🌧️"),
    "fog": ("foggy", "🌫️"),
    "sun": ("sunny", "☀️"),
    "drizzle": ("cool", "🌦️"),
    "snow": ("cool", "❄️")
}

# Custom CSS for styling and background
st.markdown("""
<style>
    .stApp {
        background-color: #F0F5FA;
        font-family: Arial, sans-serif;
    }
    .main-header {
        font-size: 36px;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 20px;
    }
    .animated-emoji {
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    .sub-header {
        font-size: 18px;
        color: #4682B4;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-title {
        font-size: 22px;
        color: #2E86C1;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #E6F0FA;
    }
    .sidebar-header {
        font-size: 20px;
        color: #2E86C1;
        margin-bottom: 15px;
    }
    .about-text {
        font-size: 14px;
        color: #555;
        margin-top: 20px;
        padding: 10px;
        background-color: #FFFFFF;
        border-radius: 5px;
    }
    .prediction-text {
        font-size: 24px;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title with animated emoji
st.markdown("<div class='main-header'><span class='animated-emoji'>🌦️</span> Seattle Weather Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Simple and accurate weather predictions for Seattle</div>", unsafe_allow_html=True)

# Load model and encoder
try:
    with open("weather_model.pkl", "rb") as f:
        model = pickle.load(f)
    label_encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    st.error("Model or encoder files not found. Please ensure 'weather_model.pkl' and 'label_encoder.pkl' are in the directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model or encoder: {str(e)}")
    st.stop()

# Load dataset for historical analysis
try:
    df = pd.read_csv("seattle-weather.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    years = sorted(df['year'].unique().tolist())
    min_temp = float(df['temp_min'].min())
    max_temp = float(df['temp_max'].max())
except FileNotFoundError:
    df = None
    years = []
    min_temp, max_temp = -5.0, 35.0
    st.warning("Historical data not found. Some features may be limited.")

# Sidebar: Slicers and Inputs
with st.sidebar:
    st.markdown("<div class='sidebar-header'>Settings</div>", unsafe_allow_html=True)
    
    st.markdown("### Input Weather Data")
    with st.form(key="weather_form"):
        precipitation = st.number_input("Precipitation (mm)", min_value=0.0, max_value=50.0, value=0.0, step=0.1)
        temp_max = st.number_input("Max Temp (°C)", min_value=-5.0, max_value=35.0, value=15.0, step=0.1)
        temp_min = st.number_input("Min Temp (°C)", min_value=-5.0, max_value=25.0, value=10.0, step=0.1)
        wind = st.number_input("Wind (km/h)", min_value=0.0, max_value=30.0, value=5.0, step=0.1)
        submit_button = st.form_submit_button("Predict Weather")

    st.markdown("### Filters")
    selected_year = st.selectbox("Select Year", options=years if years else ["All"], index=0)
    temp_range = st.slider("Temperature Range (°C)", min_value=min_temp, max_value=max_temp, value=(min_temp, max_temp))

    # About This Application
    st.markdown("<div class='about-text'>", unsafe_allow_html=True)
    st.markdown("### About This Application")
    st.markdown("""
    - **Purpose**: This dashboard predicts Seattle's weather (rain, fog, sun, drizzle, snow) using a RandomForest model.
    - **Model**: Trained on historical weather data with features like precipitation, temperature, and wind.
    - **Data Source**: Seattle Weather Dataset.
    - **Features**: Interactive predictions, historical trends, and customizable filters for year and temperature range.
    - Powered by xAI's advanced machine learning technology.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Filter data based on slicers
if df is not None:
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    filtered_df = filtered_df[(filtered_df['temp_max'] >= temp_range[0]) & (filtered_df['temp_max'] <= temp_range[1])]

# Prediction and Graphs
if submit_button:
    # Validate inputs
    if any(pd.isna([precipitation, temp_max, temp_min, wind])):
        st.error("Please fill in all fields with valid numbers.")
    else:
        # Prepare input data
        input_data = pd.DataFrame({
            "precipitation": [precipitation],
            "temp_max": [temp_max],
            "temp_min": [temp_min],
            "wind": [wind]
        })

        # Prediction with animation
        with st.spinner("Analyzing weather conditions..."):
            time.sleep(1)
            try:
                prediction = model.predict(input_data)[0]
                prediction_label = label_encoder.inverse_transform([prediction])[0]
                category, emoji = WEATHER_CATEGORIES.get(prediction_label, ("unknown", "❓"))

                # Probabilities
                probabilities = model.predict_proba(input_data)[0]
                prob_df = pd.DataFrame({
                    "Weather": label_encoder.classes_,
                    "Probability": probabilities
                })

                # Save prediction to history
                prediction_record = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Precipitation": precipitation,
                    "Max Temp": temp_max,
                    "Min Temp": temp_min,
                    "Wind": wind,
                    "Predicted Weather": category
                }
                prediction_df = pd.DataFrame([prediction_record])
                history_file = "prediction_history.csv"
                if os.path.exists(history_file):
                    prediction_history = pd.read_csv(history_file)
                else:
                    prediction_history = pd.DataFrame()
                prediction_history = pd.concat([prediction_history, prediction_df], ignore_index=True)
                prediction_history.to_csv(history_file, index=False)

                # Display prediction with user-friendly category and emoji
                st.markdown("<div class='section-title'>Prediction</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='prediction-text'>It's {category} {emoji}</div>", unsafe_allow_html=True)

                # Weather Probabilities (Pie Chart) with legend to avoid overlap
                st.markdown("<div class='section-title'>Weather Probabilities</div>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(6, 6))
                wedges, texts, autotexts = ax.pie(prob_df["Probability"], autopct="%1.1f%%", colors=sns.color_palette("pastel"))
                ax.axis("equal")
                # Add a legend instead of direct labels
                ax.legend(wedges, prob_df["Weather"], title="Weather Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                for autotext in autotexts:
                    autotext.set_fontsize(10)
                st.pyplot(fig)

                # Feature Importance (Bar Chart)
                st.markdown("<div class='section-title'>Feature Importance</div>", unsafe_allow_html=True)
                feature_importance = model.feature_importances_
                features = ["Precipitation", "Max Temp", "Min Temp", "Wind"]
                fig, ax = plt.subplots(figsize=(6, 3))
                sns.barplot(x=feature_importance, y=features, ax=ax, palette="pastel")
                ax.set_xlabel("Importance")
                st.pyplot(fig)

                # Temperature Trend (Line Chart) if data available
                if df is not None and not filtered_df.empty:
                    st.markdown("<div class='section-title'>Temperature Trend</div>", unsafe_allow_html=True)
                    temp_trend = filtered_df.groupby("date")[["temp_max", "temp_min"]].mean()
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(temp_trend.index, temp_trend["temp_max"], label="Max Temp", color="red", marker="o")
                    ax.plot(temp_trend.index, temp_trend["temp_min"], label="Min Temp", color="blue", marker="o")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Temperature (°C)")
                    ax.legend()
                    ax.grid(True)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                else:
                    st.warning("No data available for the selected filters.")

                # Prediction History
                st.markdown("<div class='section-title'>Prediction History</div>", unsafe_allow_html=True)
                st.dataframe(prediction_history.style.set_properties(**{'text-align': 'center'}))

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

# Footer
st.markdown("<hr style='border: 1px solid #2E86C1;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4682B4;'>Built with ❤️ using Streamlit | Data: Seattle Weather Dataset</p>", unsafe_allow_html=True)
