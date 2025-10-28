from machine import ADC, Pin, I2C
import network
import urequests
import time
from i2c_lcd import I2cLcd
from keypad import Keypad  # custom keypad driver

# ---------------- Soil Sensors ----------------
sensor1 = ADC(26)
sensor2 = ADC(27)

# ---------------- Relay (Active LOW: 0 = ON, 1 = OFF) ----------------
relay = Pin(7, Pin.OUT)
relay.value(1)  # Start with pump OFF

# ---------------- Thresholds ----------------
MOISTURE_THRESHOLD = 50000
RAIN_THRESHOLD = 60
PUMP_RUNTIME = 3   # used in auto irrigation

# ---------------- Wi-Fi ----------------
SSID = "VK NARZO"
PASSWORD = "aann1230"

# ---------------- WeatherAPI ----------------
API_KEY = "41af0d5cbfcd421f8b233725251309"
LAT = "10.3333"
LON = "76.2333"
URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LAT},{LON}&days=1"

# ---------------- I2C LCD ----------------
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# ---------------- Keypad ----------------
rows = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in (2,3,4,5)]
cols = [Pin(x, Pin.OUT) for x in (6,8,9,10)]
keys = [['1','2','3','A'],
        ['4','5','6','B'],
        ['7','8','9','C'],
        ['*','0','#','D']]
keypad = Keypad(rows, cols, keys)

# ---------------- Functions ----------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    lcd.clear()
    lcd.putstr("Connecting WiFi")
    while not wlan.isconnected():
        time.sleep(1)
    lcd.clear()
    lcd.putstr("WiFi Connected")
    print("✅ WiFi Connected:", wlan.ifconfig()[0])
    time.sleep(1)

def get_rain_probability():
    try:
        response = urequests.get(URL)
        data = response.json()
        response.close()
        rain_prob = int(data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"])
        print(f"🌧 Rain Probability: {rain_prob}%")
        return rain_prob
    except Exception as e:
        print("❌ API Error:", e)
        return None

def read_soil():
    m1 = sensor1.read_u16()
    m2 = sensor2.read_u16()
    avg = (m1 + m2) // 2
    return avg

def irrigate_once():
    """Pump ON only for limited runtime"""
    lcd.clear()
    lcd.putstr("💧 Pump ON")
    print("💧 Pump ON")
    relay.value(0)  # ON
    time.sleep(PUMP_RUNTIME)
    relay.value(1)  # OFF
    lcd.clear()
    lcd.putstr("⛔ Pump OFF")
    print("⛔ Pump OFF")
    time.sleep(2)

def pump_on_manual():
    relay.value(0)
    lcd.clear()
    lcd.putstr("💧 Pump MANUAL ON")
    print("💧 Pump MANUAL ON")
    time.sleep(2)

def pump_off_manual():
    relay.value(1)
    lcd.clear()
    lcd.putstr("⛔ Pump MANUAL OFF")
    print("⛔ Pump MANUAL OFF")
    time.sleep(2)

# ---------------- Modes ----------------
def mode_soil():
    """Continuously monitor soil and irrigate until # is pressed"""
    lcd.clear()
    lcd.putstr("Soil Mode Active")
    time.sleep(1)

    while True:
        soil = read_soil()
        lcd.clear()
        lcd.putstr(f"Soil:{soil}")
        lcd.move_to(0,1)
        lcd.putstr(f"Th:{MOISTURE_THRESHOLD}")

        if soil < MOISTURE_THRESHOLD:
            # Soil wet → Pump OFF
            relay.value(1)
            print("Soil wet → Pump OFF")
            lcd.move_to(0,1)
            lcd.putstr("Soil Wet       ")
        else:
            # Soil dry → Pump ON
            relay.value(0)
            print("Soil dry → Pump ON")
            lcd.move_to(0,1)
            lcd.putstr("Soil Dry → Pump")

        # Exit mode when '#' pressed
        key = keypad.get_key()
        if key == '#':
            relay.value(1)  # Always stop pump
            lcd.clear()
            lcd.putstr("Exiting SoilMode")
            time.sleep(2)
            break

        time.sleep(1)

def mode_rain():
    rain_prob = get_rain_probability()
    lcd.clear()
    if rain_prob is None:
        lcd.putstr("Rain:Error   ")
    else:
        lcd.putstr(f"Rain:{rain_prob}%")
        lcd.move_to(0,1)
        lcd.putstr(f"Th:{RAIN_THRESHOLD}%")
    time.sleep(3)

def mode_both():
    soil = read_soil()
    rain_prob = get_rain_probability()
    lcd.clear()
    lcd.putstr(f"Soil:{soil}")
    lcd.move_to(0,1)
    if rain_prob is None:
        lcd.putstr("Rain:Error   ")
        time.sleep(2)
        return
    lcd.putstr(f"Rain:{rain_prob}%")
    if soil >= MOISTURE_THRESHOLD and rain_prob < RAIN_THRESHOLD:
        irrigate_once()
    else:
        lcd.move_to(0,1)
        lcd.putstr("Skip Irrigation")
        time.sleep(2)

# ---------------- Main ----------------
def main():
    connect_wifi()

    while True:
        lcd.clear()
        lcd.putstr("Select Mode:\n1-S 2-R 3-B")
        time.sleep(0.5)

        key = None
        while key is None:
            key = keypad.get_key()
            time.sleep(0.1)

        lcd.clear()
        lcd.putstr("Mode: " + key)
        print("Mode Selected:", key)
        time.sleep(0.5)

        if key == '1':
            mode_soil()
        elif key == '2':
            mode_rain()
        elif key == '3':
            mode_both()
        elif key == '4':
            pump_on_manual()
        elif key == '5':
            pump_off_manual()
        elif key == '6':
            lcd.clear()
            lcd.putstr("Reconnecting...")
            connect_wifi()
        elif key == '#':
            lcd.clear()
            lcd.putstr("Returning...")
            time.sleep(2)

# ---------------- Run ----------------
if __name__ == "__main__":
    main()
