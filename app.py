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

# Custom CSS for colorful design
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            color: #0073e6;
            text-align: center;
        }
        .subtitle {
            font-size: 18px;
            color: #ff6347;
            text-align: center;
        }
        .metric-text {
            color: #32cd32;
            font-weight: bold;
        }
        .alert-box {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #f5c6cb;
            padding: 10px;
        }
        .chart-container {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Subtitle
st.markdown('<div class="title">🩺 Smart Band - Health Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time monitoring of **Oxygen Saturation (SpO2)** and **Heart Rate (BPM)**.</div>', unsafe_allow_html=True)
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
    if st.button("▶️ Start Monitoring", use_container_width=True, key="start", help="Start live monitoring of SpO2 and BPM", disabled=st.session_state.monitoring):
        st.session_state.monitoring = True
with col2:
    if st.button("⏹️ Stop Monitoring", use_container_width=True, key="stop", help="Stop live monitoring", disabled=not st.session_state.monitoring):
        st.session_state.monitoring = False

# =============================
# Alert Box
# =============================
alert_box = st.empty()

# =============================
# Metric Display
# =============================
col1, col2 = st.columns(2)
spo2_metric = col1.metric("🫁 SpO2 (%)", "—", help="Current oxygen saturation level")
bpm_metric = col2.metric("❤️ Heart Rate (BPM)", "—", help="Current heart rate in beats per minute")

# =============================
# Chart Area
# =============================
with st.container():
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    chart_area = st.line_chart(st.session_state.data, x="Time", y=["SpO2", "BPM"])
    st.markdown('</div>', unsafe_allow_html=True)

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
                alert_box.markdown(f'<div class="alert-box">⚠️ Low SpO2 detected: {spo2:.1f}%</div>', unsafe_allow_html=True)
            elif bpm < BPM_LOW or bpm > BPM_HIGH:
                alert_box.markdown(f'<div class="alert-box">⚠️ Abnormal Heart Rate: {bpm} BPM</div>', unsafe_allow_html=True)
            else:
                alert_box.success("✅ Vitals are in healthy range.")
        else:
            alert_box.warning("⚠️ Received malformed data.")
    except Exception as e:
        alert_box.error(f"❌ Error reading sensor: {e}")

    time.sleep(1)
    st.rerun()
