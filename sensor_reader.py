import os

def is_running_in_cloud():
    return os.getenv("STREAMLIT_CLOUD") == "1"

if not is_running_in_cloud():
    try:
        import serial
        ser = serial.Serial('COM3', 115200)
    except Exception as e:
        print(f"⚠️ Could not connect to serial port: {e}")
        ser = None
else:
    ser = None
    print("✅ Running in cloud — using mock data.")

def read_hardware_data():
    if ser:
        try:
            line = ser.readline().decode().strip()
            return line
        except Exception as e:
            return f"Error reading from sensor: {e}"
    else:
        # Provide simulated data
        return "97.5,80"  # e.g., SpO2=97.5%,
