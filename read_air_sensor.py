import time
from sensor.sds011 import *
import aqi
import os
from flask import Flask
from flask_apscheduler import APScheduler
from db_connection import write_points

scheduler = APScheduler()
app = Flask(__name__)
# turn_off_usb_cmd = 'sudo /home/pi/juan/uhubctl/uhubctl -l 1-1 -a off'
# turn_on_usb_cmd = 'sudo /home/pi/juan/uhubctl/uhubctl -l 1-1 -a on'

@scheduler.task('cron', id='read_scheduler', day='*', hour='*', minute='*/10')
def read():
    data = get_data()
    print(f"Air pollution - Raw: {data}")
    data_human = conv_aqi(data[0], data[1])
    print(f"Air pollution - human: {data_human}")
    write_to_db(data_human[0], data_human[1])

def get_data():
    sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
    sensor.sleep(sleep=False)
    time.sleep(10)
    pm_2_5, pm_10 = sensor.query()
    sensor.sleep(sleep=True)
    return pm_2_5, pm_10


def conv_aqi(pmt_2_5, pmt_10):
    aqi_2_5_epa = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
    aqi_10_epa = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
    aqi_2_5_china = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5), algo=aqi.ALGO_MEP)
    aqi_10_china = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10), algo=aqi.ALGO_MEP)
    return aqi_2_5, aqi_10

def write_to_db(pm_2_5, pm_10):
    data_write = {'pm_2_5': pm_2_5,
                  'pm_10': pm_10
                  }
    write_points(measurement='air_pollution', sensor_location='Wintergarten', **data_write)

scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=False)

