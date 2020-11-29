import time
from sensor.sds011 import *
import aqi
# import os
from flask import Flask
from flask_apscheduler import APScheduler
from db_connection import write_points

scheduler = APScheduler()
app = Flask(__name__)
# turn_off_usb_cmd = 'sudo /home/pi/juan/uhubctl/uhubctl -l 1-1 -a off'
# turn_on_usb_cmd = 'sudo /home/pi/juan/uhubctl/uhubctl -l 1-1 -a on'


def get_data():
    sensor.sleep(sleep=False)
    time.sleep(10)
    pm_2_5, pm_10 = sensor.query()
    sensor.sleep(sleep=True)
    return pm_2_5, pm_10


def conv_aqi(pmt_2_5, pmt_10):
    aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
    aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
    return aqi_2_5, aqi_10


def write_to_db(pm_2_5, pm_10):
    print(f"PM2.5: {pm_2_5}, PM10: {pm_10}")
    data_write = {'pm_2_5': pm_2_5,
                  'pm_10': pm_10
                  }
    write_points(measurement='air_pollution', sensor_location='Wintergarten', **data_write)


@scheduler.task('cron', id='read_scheduler', day='*', hour='*', minute='*/1')
def read():
    print("Attempt to read data..")
    data = get_data()
    print(f"Air pollution - Raw: {data}")
    data_human = conv_aqi(data[0], data[1])
    print(f"Air pollution - human: {data_human}")
    write_to_db(data_human[0], data_human[1])


scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
    app.run(host="0.0.0.0", debug=False)
