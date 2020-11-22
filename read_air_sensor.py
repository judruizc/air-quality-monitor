import time
from datetime import datetime
from sensor.sds011 import *
import aqi
# from db_connection import write_points

sensor = SDS011("/dev/ttyUSB1", use_query_mode=True)

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

# def write_to_db(pm_2_5, pm_10):
#     data_write = {'pm_2_5': pm_2_5,
#                   'pm_10': pm_10
#                   }
#
#     write_points(measurement='air_pollution', sensor_location='Wintergarden', **data_write)


def main():
    for i in range (4):
        data = get_data()
        print(f"Air pollution - Raw: {data}")
        data_human = conv_aqi(data[0], data[1])
        print(f"Air pollution - human: {data_human}")
        time.sleep(2)

if __name__ == '__main__':
    main()


            
