import streamlit as st
import time
from sensor_reader import read_hardware_data as generate_data

st.set_page_config(page_title="Smart Health Monitor", layout="centered")

st.title("🩺 Smart Band - Health Monitor")
st.markdown("Monitoring real-time **Oxygen Saturation (SpO2)** and **Heart Rate (BPM)**.")

# Placeholders for dynamic values
spo2_display = st.empty()
bpm_display = st.empty()
status_display = st.empty()

# Start button
if st.button("Start Monitoring"):
    st.success("🟢 Monitoring started. Receiving data from sensor...")

    while True:
        try:
            data = generate_data()

            # Expecting "97.3,82" format
            if "," in data:
                spo2_val, bpm_val = data.strip().split(",")
                spo2_val = float(spo2_val)
                bpm_val = int(bpm_val)

                spo2_display.metric(label="SpO2 (%)", value=f"{spo2_val:.1f} %", delta=None)
                bpm_display.metric(label="Heart Rate (BPM)", value=f"{bpm_val} BPM", delta=None)
                status_display.success("✅ Data received successfully.")

            else:
                status_display.warning(f"Unexpected data format: `{data}`")

        except Exception as e:
            status_display.error(f"❌ Error reading data: {e}")

        time.sleep(1)
