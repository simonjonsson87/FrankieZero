import adafruit_ahtx0
import board
import time, requests, json
from Utils import *
from SimonsBMP280 import *
from SimonsDisplay import *
from SimonsApiComm import *
from datetime import datetime
from SimonsSDS011 import SimonsSDS011

# Setup I2C Sensor
AHT20 = adafruit_ahtx0.AHTx0(board.I2C())

CONFIG_FILE = "/home/pi/FrankieV2/config.conf"
CONF = json.load(open(CONFIG_FILE, "r"))

SDS011 = SimonsSDS011()

while True:
    startT = time.time()
    #
    # BMP280 readings
    bmp_temp,bmp_pressure,bmp_humidity = readBME280All()
    sensor = "BMP280"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api("Temperature", CONF, sensor, dt, bmp_temp)
    api("Humidity", CONF, sensor, dt, bmp_humidity)
    api("Pressure", CONF, sensor, dt, bmp_pressure)

    #
    # AHT20 readings
    aht_temp = AHT20.temperature
    aht_humidity = AHT20.relative_humidity
    sensor = "AHT20"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api("Temperature", CONF, sensor, dt, aht_temp)
    api("Humidity", CONF, sensor, dt, aht_humidity)

    #
    # Air particles
    pm25, pm10, sds_ok = SDS011.getReading()
    sensor = "SDS011"
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api_AirParticles(CONF, sensor, dt, pm25, pm10, sds_ok)

    #
    # Print in console
    print('AHT20_Temperature', round_num(aht_temp), 'C')
    print('AHT20_Humidity', round_num(aht_humidity), '%')
    print('BMP280_Temperature', round_num(bmp_temp), 'C')
    print('BMP280_Humidity', round_num(bmp_humidity), '%')
    print('BMP280_Pressure', str(int(bmp_pressure)), 'hPa')
    print('SDS011_Paricles small=', str(pm25), 'big=', str(pm10), sds_ok)


    #
    # Draw on display
    #drawSensorStats(aht_temp, bmp_pressure, aht_humidity, dt)
    #dt = datetime.now().strftime("%H:%M:%S")
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    drawSensorStatsV2(aht_temp, bmp_pressure, aht_humidity, dt, pm25, pm10)

    time.sleep(60*5)
