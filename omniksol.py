import network
import urequests
import time
from machine import Pin

led = Pin("LED", Pin.OUT)

# Wi-Fi configuration
SSID = "add your sidd"
PASSWORD = "add your password"

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        
        while not wlan.isconnected():
            pass
    
    print("Connected to WiFi:", wlan.ifconfig())

def fetch_data(url):
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.text
            # Extract the desired field using similar logic as 'cut -d '"' -f16'
            fields = data.split('"')
            if len(fields) > 15:  # Ensure there are enough fields to index into
                all_fields = fields[15]
                #print("Extracted Data:", all_fields)#debug
                # Further split by space within each field if needed
                sub_fields = all_fields.split(',')
                #print(sub_fields)#debug
                print("Inverter serial number:", sub_fields[0])
                print("Firmware version (main):", sub_fields[1])
                print("Firmware version (slave):", sub_fields[2])
                print("Inverter model:", sub_fields[3])
                print("Rated power:", sub_fields[4], "W")
                print("Current power:", sub_fields[5], "W")
                print("Yield today:",(int(sub_fields[6]) / 100), "kWh")
                print("Total yield:", (int(sub_fields[7]) / 10), "kWh")
                print("Alerts:", sub_fields[8])
                print("Last updated:", sub_fields[9], "Min Ago")
                #switch the led if current power is above ....
                if int(sub_fields[5]) > 500:
                    led.value(1)
                else:
                    led.value(0)
            else:
                print("Not enough fields in the response")
                led.value(0)
        else:
            print(f"Failed to fetch data, status code: {response.status_code}")
            led.value(0)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    connect_to_wifi(SSID, PASSWORD)
    while True:
        url = "http://10.10.100.254/js/status.js"
        fetch_data(url)
        time.sleep(60 * 5)
