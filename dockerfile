FROM python:3.7-slim
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . /home_sensors
WORKDIR /home_sensors
CMD ["python", "read_air_sensor.py"]
