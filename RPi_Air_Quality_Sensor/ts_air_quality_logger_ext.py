import time
from datetime import datetime
from RPi_Air_Quality_Sensor.sds011 import *
import aqi

sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)

def get_data(n=3):
        sensor.sleep(sleep=False)
        pmt_2_5 = 0
        pmt_10 = 0
        time.sleep(10)
        for i in range (n):
            x = sensor.query()
            pmt_2_5 = pmt_2_5 + x[0]
            pmt_10 = pmt_10 + x[1]
            time.sleep(2)
        pmt_2_5 = round(pmt_2_5/n, 1)
        pmt_10 = round(pmt_10/n, 1)
        sensor.sleep(sleep=True)
        time.sleep(2)
        return pmt_2_5, pmt_10
    

def conv_aqi(pmt_2_5, pmt_10):
    aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
    aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
    return aqi_2_5, aqi_10


def save_log():        
    with open("/Users/juan.ruiz/Projects/Personal/air-quality-monitor/air_quality.csv", "a") as log:
        dt = datetime.now()
        log.write("{},{},{},{},{}\n".format(dt, pmt_2_5, aqi_2_5, pmt_10, aqi_10))
    log.close()


data = get_data(3)
print(f"Air pollution - Raw: {data}")
data_human = conv_aqi(data)
print(f"Air pollution - human: {data_human}")

            