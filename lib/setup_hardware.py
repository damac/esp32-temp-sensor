from microcontroller import Pin
import adafruit_bmp280
import json
import wifi
import os
import time
import socketpool
import adafruit_requests
import ssl


class WifiContext:
    request: adafruit_requests.Session
    mac_address: str


def initialize_bmp(i2c: busio.I2C, address: hex) -> adafruit_bmp280:
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address)
    bmp280.sea_level_pressure = 1029.05
    bmp280.mode = adafruit_bmp280.MODE_NORMAL
    bmp280.standby_period = adafruit_bmp280.STANDBY_TC_500
    bmp280.iir_filter = adafruit_bmp280.IIR_FILTER_X16
    bmp280.overscan_pressure = adafruit_bmp280.OVERSCAN_X16
    bmp280.overscan_temperature = adafruit_bmp280.OVERSCAN_X2
    # The sensor will need a moment to gather inital readings
    time.sleep(1)
    return bmp280


def gather_temp_reading(bmp280: adafruit_bmp280, mac: str) -> dict:
    freedom_temp = ((9 / 5) * bmp280.temperature) + 32
    data = {
        'state': freedom_temp,
        'attributes':
            {
                'unit_of_measurement': "°F"
            },
        'unique_id': mac}
    return data


def gather_pressure_reading(bmp280: adafruit_bmp280, mac: str) -> dict:
    data = {
        'state': bmp280.pressure,
        'attributes':
            {
                'unit_of_measurement': "hPa"
            },
        'unique_id': mac}
    return data


def update_home_assistant(entity_id, data, wifi_ctx):

    url = os.getenv('HOME_ASSISTANT_URL') + "/api/states/sensor." + entity_id
    headers = {"Authorization": "Bearer " + os.getenv('HOME_ASSISTANT_JWT', '')}
    response = wifi_ctx.request.post(url, data=json.dumps(data), headers=headers)
    print(response.status_code)


def init_wifi():
    ctx = WifiContext()
    wifi.radio.start_scanning_networks()
    wifi.radio.stop_scanning_networks()

    mac = ''
    for i in wifi.radio.mac_address:
        mac = mac + hex(i).replace('0x', '') + ":"

    ctx.mac_address = mac[:-1]

    print(wifi.radio.connect(ssid=os.getenv('CIRCUITPY_WIFI_SSID'), password=os.getenv('CIRCUITPY_WIFI_PASSWORD')))
    print("my IP addr:", wifi.radio.ipv4_address)
    print(ctx.mac_address)
    pool = socketpool.SocketPool(wifi.radio)
    ctx.request = adafruit_requests.Session(pool, ssl.create_default_context())

    return ctx

