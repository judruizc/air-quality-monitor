import time
from datetime import datetime
from sensor.sds011 import *
import aqi
from db_connection import write_points

sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)

def get_data(n=3):
        sensor.sleep(read=True, sleep=False)
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

def write_to_db(pm_2_5, pm_10):
    data_write = {'pm_2_5': pm_2_5,
                  'pm_10': pm_10
                  }

    write_points(measurement='air_pollution', sensor_location='Wintergarden', **data_write)


def main():
    data = get_data(3)
    print(f"Air pollution - Raw: {data}")
    data_human = conv_aqi(data[0], data[1])
    print(f"Air pollution - human: {data_human}")


if __name__ == '__main__':
    main()


            
