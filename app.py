# =============================
# PART 1: Simulated Data Generator
# =============================
import random
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import streamlit as st
import numpy as np
import time
from sklearn.preprocessing import MinMaxScaler

def generate_data():
    return {
        "spo2": round(random.uniform(88, 98), 1),
        "heart_rate": random.randint(60, 110),
        "resp_rate": random.randint(12, 24)
    }

# =============================
# PART 2: VAE Model
# =============================
class VAE(nn.Module):
    def __init__(self, input_dim=3, latent_dim=2):
        super(VAE, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)
        self.fc21 = nn.Linear(16, latent_dim)
        self.fc22 = nn.Linear(16, latent_dim)
        self.fc3 = nn.Linear(latent_dim, 16)
        self.fc4 = nn.Linear(16, input_dim)

    def encode(self, x):
        h1 = torch.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h3 = torch.relu(self.fc3(z))
        return self.fc4(h3)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

def loss_function(recon_x, x, mu, logvar):
    BCE = nn.functional.mse_loss(recon_x, x, reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + KLD

# =============================
# PART 3: Training VAE Model
# =============================
scaler = MinMaxScaler()
data = np.array([list(generate_data().values()) for _ in range(1000)])
data = scaler.fit_transform(data)

vae = VAE()
optimizer = optim.Adam(vae.parameters(), lr=0.001)

def train_vae(model, data, epochs=10):
    for epoch in range(epochs):
        total_loss = 0
        for x in data:
            x = torch.tensor(x, dtype=torch.float32)
            optimizer.zero_grad()
            recon, mu, logvar = model(x)
            loss = loss_function(recon, x, mu, logvar)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}: Loss = {total_loss:.2f}")

train_vae(vae, data)

# =============================
# PART 4: Streamlit Real-Time Dashboard
# =============================
st.title("🩺 Smart Band - ILD Patient Monitoring Dashboard")
spo2_vals, hr_vals, rr_vals, alerts = [], [], [], []

for _ in range(50):
    reading = generate_data()
    input_vals = scaler.transform([list(reading.values())])[0]
    input_tensor = torch.tensor(input_vals, dtype=torch.float32)
    recon, mu, logvar = vae(input_tensor)
    loss = loss_function(recon, input_tensor, mu, logvar).item()
    anomaly = loss > 5.0

    spo2_vals.append(reading['spo2'])
    hr_vals.append(reading['heart_rate'])
    rr_vals.append(reading['resp_rate'])
    alerts.append(anomaly)

    col1, col2 = st.columns(2)
    col1.metric("SpO₂ (%)", reading['spo2'])
    col2.metric("Heart Rate (bpm)", reading['heart_rate'])
    st.write(f"Respiratory Rate: {reading['resp_rate']} breaths/min")
    
    if anomaly:
        st.error("⚠️ Anomaly Detected - Possible Desaturation! 🚨")
    else:
        st.success("Vitals Normal ✅")

    time.sleep(1)
