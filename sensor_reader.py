#!/usr/bin/env python
import os, sys, Adafruit_DHT, time, pika, json
from datetime import datetime, date

sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
pin                          = 4
sensor_name                  = "living-room"
entry_format                 = "{:%Y-%m-%d %H:%M:%S},{:0.1f}\n"
rabbitmq_host                = "localhost"

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()
channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

while True:
  hum, temp = Adafruit_DHT.read_retry(sensor, pin)
  if hum is not None and temp is not None:
    message = json.dumps({'datetime': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.today()),
      'temperature': '{:0.1f}'.format(temp),
      'humidity': '{:0.1f}'.format(hum),
      'sensor_name': sensor_name})
    channel.basic_publish(exchange='temp_and_humidity',
      routing_key='',
      body=message)
  time.sleep(60)

connection.close()
