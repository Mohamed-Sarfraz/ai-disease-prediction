import streamlit as st
import time
from datetime import datetime
import pandas as pd
import random

# =============================
# Simulated Data Generator
# =============================
def generate_data():
    # Simulating the sensor data: SpO2 and Heart Rate
    spo2 = round(random.uniform(88, 98), 1)
    bpm = random.randint(60, 110)
    return f"{spo2},{bpm}"

# =============================
# Page Config
# =============================
st.set_page_config(page_title="Smart Health Monitor", layout="centered")

# App Title and Subtitle
st.title("🩺 Smart Band - Health Monitor")
st.markdown("Real-time monitoring of **Oxygen Saturation (SpO2)** and **Heart Rate (BPM)**.")
st.divider()

# =============================
# Thresholds
# =============================
SPO2_ALERT_THRESHOLD = 95
BPM_LOW = 60
BPM_HIGH = 100

# =============================
# App State (persistent during session)
# =============================
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

# Data storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "SpO2", "BPM"])

# =============================
# Control Buttons
# =============================
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Monitoring", use_container_width=True):
        st.session_state.monitoring = True
with col2:
    if st.button("⏹️ Stop Monitoring", use_container_width=True):
        st.session_state.monitoring = False

# =============================
# Alert Box
# =============================
alert_box = st.empty()

# =============================
# Metric Display
# =============================
col1, col2 = st.columns(2)
spo2_metric = col1.metric("🫁 SpO2 (%)", "—")
bpm_metric = col2.metric("❤️ Heart Rate (BPM)", "—")

# =============================
# Chart Area
# =============================
chart_area = st.line_chart(st.session_state.data, x="Time", y=["SpO2", "BPM"])

# =============================
# Loop for Live Update
# =============================
while st.session_state.monitoring:
    try:
        raw_data = generate_data()  # Fetch sensor data (simulated here)
        if "," in raw_data:
            spo2_str, bpm_str = raw_data.strip().split(",")
            spo2 = float(spo2_str)
            bpm = int(bpm_str)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Update data
            new_row = {"Time": timestamp, "SpO2": spo2, "BPM": bpm}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

            # Keep last 30 points
            if len(st.session_state.data) > 30:
                st.session_state.data = st.session_state.data.iloc[-30:]

            # Update Metrics
            spo2_metric.metric("🫁 SpO2 (%)", f"{spo2:.1f}")
            bpm_metric.metric("❤️ Heart Rate (BPM)", f"{bpm} BPM")

            # Update Chart
            chart_area.line_chart(st.session_state.data.set_index("Time")[["SpO2", "BPM"]])

            # =============================
            # Alert Conditions
            # =============================
            if spo2 < SPO2_ALERT_THRESHOLD:
                alert_box.error(f"⚠️ Low SpO2 detected: {spo2:.1f}%")
            elif bpm < BPM_LOW or bpm > BPM_HIGH:
                alert_box.warning(f"⚠️ Abnormal Heart Rate: {bpm} BPM")
            else:
                alert_box.success("✅ Vitals are in healthy range.")
        else:
            alert_box.warning("⚠️ Received malformed data.")
    except Exception as e:
        alert_box.error(f"❌ Error reading sensor: {e}")

    time.sleep(1)
    st.experimental_rerun()

     
