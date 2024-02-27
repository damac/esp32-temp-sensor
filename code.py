import wifi
import board
import busio
from lib.setup_hardware import *

ENTITY_ID_NAME = "bmp280_unit_1_"
i2c = busio.I2C(board.SCL, board.SDA)
wifi_ctx = init_wifi()
sensor_bmp280 = initialize_bmp(i2c, 0x76)

while True:
    update_home_assistant(ENTITY_ID_NAME + "temp", gather_temp_reading(sensor_bmp280, wifi_ctx.mac_address), wifi_ctx)
    update_home_assistant(ENTITY_ID_NAME + "pressure", gather_pressure_reading(sensor_bmp280, wifi_ctx.mac_address), wifi_ctx)
    time.sleep(30)
