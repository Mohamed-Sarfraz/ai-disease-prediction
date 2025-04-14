import serial

# Update 'COM3' to your actual port (check Arduino IDE > Tools > Port)
ser = serial.Serial('COM3', 115200)

def read_hardware_data():
    line = ser.readline().decode('utf-8').strip()
    try:
        spo2, heart_rate, resp_rate = map(float, line.split(','))
        return {
            "spo2": spo2,
            "heart_rate": heart_rate,
            "resp_rate": resp_rate
        }
    except:
        return {"spo2": 95, "heart_rate": 80, "resp_rate": 18}  # fallback
