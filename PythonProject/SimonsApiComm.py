import requests

def api(type, CONF, sensor, reading_time, value):
    if type == "Temperature":
        url = CONF['API_BASE_URL'] + "/insertTemperature"
    elif type == "Humidity":
        url = CONF['API_BASE_URL'] + "/insertHumidity"
    elif type == "Pressure":
        url = CONF['API_BASE_URL'] + "/insertPressure"
        

    data = {'iot_name': CONF['IOT_NAME'], 'time': reading_time, 'sensor_name': sensor, 'value': value}

    try:
        x = requests.post(url, json = data, timeout=5)
        print(x)
    except Exception as e:
        print("SimonsApiComm:api - The request ended in an exception: ")
        print(e)
   
def api_AirParticles(CONF, sensor, reading_time, pm25, pm10, sds_ok):

    data = {'iot_name': CONF['IOT_NAME'], 'time': reading_time, 'sensor_name': sensor, 'pm25': pm25, 'pm10': pm10, 'checksum_ok': sds_ok}
    url = CONF['API_BASE_URL'] + "/insertAirParticles"
    try:
        x = requests.post(url, json = data, timeout=5)
        print(x)
    except Exception as e:
        print("SimonsApiComm:api_AirParticles - The request ended in an exception: ")
        print(e)