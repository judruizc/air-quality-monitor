from influxdb import InfluxDBClient
import requests
import sys
import time
import datetime
import pprint


db_host = 'influxdb'
db_port = '8086'
db_name = 'db01'
# Initialize the global client variable
db_client = None


def db_exists():
	'''returns True if the database exists'''
	dbs = db_client.get_list_database()
	for db in dbs:
		if db['name'] == db_name:
			return True
	return False


def wait_for_server(host, port, nretries=5):
	'''wait for the server to come online for waiting_time, nretries times.'''
	url = 'http://{}:{}'.format(host, port)
	waiting_time = 1
	for i in range(nretries):
		try:
			requests.get(url)
			return
		except requests.exceptions.ConnectionError:
			print('waiting for', url)
			time.sleep(waiting_time)
			waiting_time *= 2
			pass
	print('cannot connect to', url)
	sys.exit(1)


def connect_db(host, port):
	'''connect to the database, and create it if it does not exist'''
	global db_client
	print('connecting to database: {}:{}'.format(host, port))
	db_client = InfluxDBClient(host, port, retries=5, timeout=5)
	wait_for_server(host, port)
	if not db_exists():
		print('creating database...')
		db_client.create_database(db_name)
	else:
		print('database already exists')
	db_client.switch_database(db_name)


def write_points(measurement, sensor_location, **kwargs):
	connect_db(db_host, db_port)
	fields = {}
	for key, value in kwargs.items():
		print("The value of {} is {}".format(key, value))
		fields.update({key: value})

	data = [{
		'measurement': measurement,
		'time': datetime.datetime.now(),
		'tags': {
			'sensor': sensor_location
		},
		'fields': fields,
	}]
	db_client.write_points(data)
	pprint.pprint(data)
	time.sleep(1)
	db_client.close()
	print("Close DB connection")
