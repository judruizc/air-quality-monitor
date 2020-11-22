FROM python:3.7-slim
COPY requirements.txt /
RUN pip install -r /requirements.txt
ADD . /home_sensors
WORKDIR /home_sensors
CMD ["python", "read_air_sensor.py"]
