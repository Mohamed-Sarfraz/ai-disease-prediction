import random
import time
import torch
import torch.nn as nn
import torch.optim as optim
import streamlit as st
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# =============================
# Simulated Data Generator
# =============================
def generate_data():
    return {
        "spo2": round(random.uniform(88, 98), 1),
        "heart_rate": random.randint(60, 110),
        "resp_rate": random.randint(12, 24)
    }

# =============================
# Streamlit Dashboard
# =============================
st.title("🩺 Smart Band - ILD Patient Monitoring Dashboard")

# Collect data for chart updates
spo2_data = []
hr_data = []

for _ in range(50):
    reading = generate_data()  # Generate simulated data
    
    # Display the data to the screen
    st.write(f"SpO2: {reading['spo2']}%, Heart Rate: {reading['heart_rate']} BPM, Respiratory Rate: {reading['resp_rate']} breaths/min")
    
    # Append data for chart
    spo2_data.append(reading['spo2'])
    hr_data.append(reading['heart_rate'])

    # Update charts in real-time
    st.line_chart(spo2_data, use_container_width=True)
    st.line_chart(hr_data, use_container_width=True)

    time.sleep(1)
