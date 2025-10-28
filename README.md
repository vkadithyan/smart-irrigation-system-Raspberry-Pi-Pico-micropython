# 🌾 Smart Irrigation System using MicroPython

An **IoT-based Smart Irrigation System** built using **MicroPython**, designed for **ESP32** or **Raspberry Pi Pico W**.  
The system intelligently controls irrigation based on **soil moisture levels**, **rain probability from WeatherAPI**, and **user-selected modes** via a **keypad** and **LCD interface**.

---

## 🚀 Features

- 🌱 **Soil Moisture Mode:**  
  Irrigation is triggered based on real-time soil sensor readings.

- 🌦 **API Mode:**  
  Fetches **rain probability** using [WeatherAPI](https://www.weatherapi.com/) and irrigates only when rainfall is unlikely.

- 💧 **Combined Mode:**  
  Considers both **soil moisture** and **rain probability** for optimized irrigation.

- 📟 **I²C LCD Display:**  
  Displays live sensor data, Wi-Fi status, rain probability, and irrigation activity.

- 🎛 **Keypad Interface:**  
  4×4 matrix keypad enables mode selection and system control:
  - `1` → Soil Moisture Mode  
  - `2` → API (Rain Probability) Mode  
  - `3` → Combined Mode  
  - `4` → Reconnect Wi-Fi  
  - `*` → Cancel / Stop  
  - `#` → Confirm Action

- ⚡ **Relay Control:**  
  Relay operates the water pump (**Active HIGH → ON, LOW → OFF**).

- 📡 **Wi-Fi Connectivity:**  
  Connects to a local Wi-Fi network to fetch live weather data.

---

## 🧠 Working Principle

1. **Connects to Wi-Fi** using predefined SSID and password.  
2. **Fetches live weather data** (rain probability) from WeatherAPI.  
3. **Reads soil moisture** from two analog sensors and calculates the average.  
4. Based on **selected mode**, decides whether irrigation is required.  
5. **Activates relay** to control the water pump for a fixed time if irrigation is needed.  
6. Displays all relevant data and actions on the **LCD**.

---

## ⚙️ Hardware Requirements

| Component | Description |
|------------|-------------|
| **ESP32 / Raspberry Pi Pico W** | Main controller board |
| **2 × Soil Moisture Sensors** | For real-time soil data |
| **16x2 I²C LCD Display** | For status display |
| **4x4 Matrix Keypad** | For user input |
| **Relay Module** | To control water pump |
| **Wi-Fi Network** | For API connectivity |

---

## 🔌 Pin Connections (Example for Raspberry Pi Pico W)

| Component | GPIO Pins Used |
|------------|----------------|
| **Soil Sensor 1** | GP26 (ADC0) |
| **Soil Sensor 2** | GP27 (ADC1) |
| **Relay (Active HIGH)** | GP7 |
| **LCD I2C (SDA, SCL)** | GP0, GP1 |
| **Keypad Rows** | GP2, GP3, GP4, GP5 |
| **Keypad Columns** | GP6, GP8, GP9, GP10 |

---

## 🌐 Weather API Setup

1. Visit [https://www.weatherapi.com/](https://www.weatherapi.com/)
2. Create a **free account**.
3. Copy your **API key** from the dashboard.
4. Update your key in the code:
   ```python
   API_KEY = "your_api_key_here"
