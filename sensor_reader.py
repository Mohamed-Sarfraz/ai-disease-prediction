import random

def read_hardware_data():
    # Since hardware can't be accessed on Streamlit Cloud,
    # this acts as a fake sensor reader
    return {
        "spo2": round(random.uniform(94, 98), 1),
        "heart_rate": random.randint(70, 95),
        "resp_rate": random.randint(14, 20)
    }
