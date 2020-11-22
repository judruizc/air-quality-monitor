FROM python:3.7-slim
COPY . /home_sensors
WORKDIR /home_sensors
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["python", "read_air_sensor.py"]
