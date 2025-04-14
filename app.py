import streamlit as st
import time
import requests
from flask import Flask, request, jsonify
from threading import Thread
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Data storage
data = pd.DataFrame(columns=["Time", "SpO2", "BPM"])

# Set up the Streamlit app
st.set_page_config(page_title="Smart Health Monitor", layout="centered")
st.title("🩺 Smart Band - Health Monitor")
st.markdown("Real-time monitoring of **Oxygen Saturation (SpO2)** and **Heart Rate (BPM)**.")

# Thresholds
SPO2_ALERT_THRESHOLD = 95
BPM_LOW = 60
BPM_HIGH = 100

# Data display
col1, col2 = st.columns(2)
spo2_metric = col1.metric("🫁 SpO2 (%)", "—")
bpm_metric = col2.metric("❤️ Heart Rate (BPM)", "—")

# Chart area
chart_area = st.line_chart(data, x="Time", y=["SpO2", "BPM"])

# Flask route to handle data from ESP32
@app.route('/data', methods=['POST'])
def receive_data():
    global data
    if request.method == 'POST':
        # Get data from the ESP32
        sensor_data = request.get_json()
        spo2 = sensor_data.get('spo2')
        bpm = sensor_data.get('bpm')

        # Get current timestamp
        timestamp = time.strftime('%H:%M:%S')

        # Update data
        new_row = {"Time": timestamp, "SpO2": spo2, "BPM": bpm}
        data = data.append(new_row, ignore_index=True)
        
        # Keep last 30 points
        if len(data) > 30:
            data = data.tail(30)

        # Update metrics
        spo2_metric.metric("🫁 SpO2 (%)", f"{spo2:.1f}")
        bpm_metric.metric("❤️ Heart Rate (BPM)", f"{bpm} BPM")

        # Update chart
        chart_area.line_chart(data.set_index("Time")[["SpO2", "BPM"]])

        # Check for alert conditions
        if spo2 < SPO2_ALERT_THRESHOLD:
            st.warning(f"⚠️ Low SpO2 detected: {spo2:.1f}%")
        elif bpm < BPM_LOW or bpm > BPM_HIGH:
            st.warning(f"⚠️ Abnormal Heart Rate: {bpm} BPM")
        else:
            st.success("✅ Vitals are in healthy range.")
        
        return jsonify({"status": "success"})

# Function to run Flask app in a background thread
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Start Flask app in the background
Thread(target=run_flask, daemon=True).start()

# Streamlit loop to keep the app alive
while True:
    time.sleep(1)
    st.experimental_rerun()

        alert_box.error(f"❌ Error reading sensor: {e}")

    time.sleep(1)
    st.rerun()
