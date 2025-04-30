# 🌦️ Seattle Weather Dashboard

An interactive Streamlit application to **predict Seattle's weather conditions** using a **Random Forest Classifier**. This dashboard provides real-time predictions, weather probabilities, feature importance analysis, and historical temperature trends.

---
![image](https://github.com/user-attachments/assets/92fa4cab-47bd-4687-98ac-b745c58f5eea)


## 📑 Overview

This project uses a pre-trained **RandomForest model** to predict one of four weather conditions in Seattle: **sunny**, **cool**, **foggy**, or **rainy**, based on inputs like:

- Precipitation (mm)
- Maximum temperature (°C)
- Minimum temperature (°C)
- Wind speed (km/h)

### 🔍 Key Visualizations:

- **Weather Prediction:** Predicts weather and shows an emoji (e.g., "It's sunny ☀️").
- **Weather Probabilities:** Pie chart of prediction probabilities.
- **Feature Importance:** Bar chart showing feature influence.
- **Temperature Trend:** Line chart showing historical temperature trends with filters.

---

## 🚀 Features

- 🔢 Real-time weather prediction using user inputs
- 📊 Visualization of probabilities and feature importance
- 🗓️ Filterable historical temperature trends by year and range
- 🧾 Logs of all past predictions with input values and timestamps
- 🎨 Animated emoji in the app title

---

## 🛠️ Setup Instructions

### 📦 Prerequisites

- Python 3.8 or higher
- Git installed
- GitHub account
- Streamlit Community Cloud account (optional for deployment)

---

### 🖥️ Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sarika-max-prog/Weather_Dashboard.git
   cd Weather_Dashboard
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies:**
   - `streamlit==1.37.0`
   - `pandas==2.2.2`
   - `scikit-learn==1.5.1`
   - `matplotlib==3.9.2`
   - `seaborn==0.13.2`

3. **Run the App Locally**
   ```bash
   streamlit run app.py
   ```

   Then open your browser and go to: [http://localhost:8501](http://localhost:8501)
   (https://weatherdashboard-bgyuzv9bxhs4yf4ktfvzxc.streamlit.app/)

---

## 📂 Required Files

Ensure the following files are present in the project directory:

- `app.py` – Main Streamlit app file
- `weather_model.pkl` – Pre-trained RandomForest model
- `label_encoder.pkl` – Label encoder for weather types
- `seattle-weather.csv` – Dataset for historical analysis
- `requirements.txt` – Python dependencies

---

## 🌐 Deployment (Streamlit Cloud)

1. Push the full project to GitHub:
   - Include all necessary files: `app.py`, model files, dataset, `requirements.txt`

2. Go to [Streamlit Community Cloud](https://share.streamlit.io)

3. Click **"New App"**

4. Select:
   - Repository: `Sarika-max-prog/Weather_Dashboard`
   - Branch: `main`
   - File: `app.py`

5. Click **Deploy**

✅ Done! Your app will be live at a URL like:

**[https://weatherdashboard-bgyuzv9bxhs4yf4ktfvzxc.streamlit.app/](https://weatherdashboard-bgyuzv9bxhs4yf4ktfvzxc.streamlit.app/)**

---

## 📊 App Usage

1. Enter weather data in the sidebar:
   - Precipitation
   - Max temperature
   - Min temperature
   - Wind speed

2. Click **Predict Weather**.

3. View:
   - Predicted condition with an emoji
   - Probabilities in a pie chart
   - Feature importance in a bar chart
   - Historical trends in a line chart

4. Check the prediction history table for logs.

---

## ⚠️ Notes

- **Prediction History:** Stored in `prediction_history.csv` (resets on each deployment in Streamlit Cloud).
- **File Size Limits:** `seattle-weather.csv` must be under 50MB for Streamlit Cloud.
- **Dependencies:** Ensure `requirements.txt` contains correct versions to avoid deployment issues.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For feedback or questions, reach out to **Sarika-max-prog** via GitHub.

---

**Built with ❤️ using Streamlit**  
**Data Source:** Seattle Weather Dataset


---

Let me know if you want me to generate a sample `LICENSE` file or a `config.toml` for customizing the app appearance!
